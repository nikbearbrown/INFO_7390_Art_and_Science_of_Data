from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from syllabus import (
    retrieve_information,
    generate_plan,
    validate_and_clean_json,
    summarize_plan,
    get_embedding,
)
from lessons import (
    retrieve_detailed_explanation,
    fetch_youtube_videos,
    fetch_video_transcript,
    upsert_to_pinecone,
    summarize_text,
    generate_embedding,
    chunk_text,
    summarize_text_arxiv
    # retrieve_from_image_index,
    # generate_text_embedding,
    # summarize_image_with_openai, 
    # generate_image_summaries
)
from utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_token,
    get_db_connection,
    get_current_username,
    get_user,
    create_user,
    inspect_index,
    YouTubeVideoResponse,
    FlashcardGeneration,
    ArxivPaperResponse,
    # SummarizationRequest,
    # ImageSummaryRequest,
    QuizGeneration,
    Module,
    Plan,
    pool,
)  
from config import (
    SNOWFLAKE_CONFIG,
    OPENAI_API_KEY,
    PINECONE_API_KEY,
    YOUTUBE_API_KEY,
    INDEX_NAME,
    YOUTUBE_INDEX,
    DIMENSION,
    METRIC,
    CLOUD_PROVIDER,
    REGION,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    client,
    pc,
    youtube,
    index,
    youtube_index,
    image_index,
    IMAGE_DIM
)
import logging
import json
from typing import Optional, List
from datetime import datetime
from fastapi_utils.tasks import repeat_every
# import torch
import tiktoken
# from transformers import CLIPProcessor, CLIPModel
# import openai

import xmltodict
import requests


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# -------- FastAPI Setup --------

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
@repeat_every(seconds=300)  # Every 5 minutes
def keep_connections_alive():
    logging.info("Running keep-alive task for Snowflake connections.")
    for _ in range(pool.pool.qsize()):
        connection = pool.get_connection()
        try:
            connection.cursor().execute("SELECT 1")
        except Exception as e:
            logging.error(f"Keep-alive task failed for a connection: {e}")
        finally:
            pool.release_connection(connection)


# --------  API Endpoints  --------
@app.post("/signup")
async def signup(username: str = Query(...), password: str = Query(...)):
    if get_user(username):
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(username, password)
    return {"message": "User created successfully"}

@app.post("/login")
async def login(username: str = Query(...), password: str = Query(...)):
    user = get_user(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer", "username": username}

@app.post("/refresh_token")
async def refresh_token(username: str = Depends(get_current_username)):
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/query")
async def query_router(request: dict):
    user_query = request.get("user_query")
    current_plan = request.get("current_plan", None)
    current_summary = request.get("current_summary", None)  # Capture the current summary to retain it

    if not user_query:
        raise HTTPException(status_code=400, detail="User query is required.")

    # Initialize response object
    response_data = {
        "plan": current_plan,  # Retain the current plan by default
        "summary": current_summary,
        "response": "Unable to process the query. Please try again later."
    }

    try:
        # Step 1: Check for relevance in the knowledge base
        context_info = retrieve_information(user_query)

        if context_info:
            # Case 1: Relevant context found → Generate/Update learning plan
            learning_plan_json = generate_plan(user_query, context_info, current_plan)
            plan = validate_and_clean_json(learning_plan_json)

            if plan:
                summary = summarize_plan(plan)

                # Generate dynamic response based on user query and context using LLM
                response_prompt = (
                    "You are a helpful assistant specializing in creating and updating learning plans. Based on the following information, "
                    "generate a professional and relevant response summarizing the action taken:\n"
                    f"User Query: {user_query}\n"
                    f"Existing Plan: {current_plan}\n"
                    f"Generated Plan: {plan}\n"
                    "Ensure the response clearly communicates the action taken and its relevance to the user's input. Be specific."
                )
                response_generation = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": response_prompt},
                        {"role": "user", "content": user_query},
                    ],
                )
                response_text = response_generation.choices[0].message.content.strip()

                response_data.update({
                    "plan": plan,
                    "summary": summary,
                    "response": response_text
                })
            else:
                response_data["response"] = "Failed to generate or parse learning plan."

        elif current_plan:
            # Case 2: Indirectly relevant query or context to refine the plan
            refine_prompt = (
                "You are an assistant specializing in refining learning plans. "
                "Determine if the user's query provides additional context to refine the current plan. "
                "If yes, generate an updated plan. If no, explain the relevance of the current plan or address the query conversationally.\n"
                f"User Query: {user_query}\n"
                f"Current Plan: {current_plan}"
            )
            refine_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": refine_prompt},
                    {"role": "user", "content": user_query},
                ],
            )

            refinement = refine_response.choices[0].message.content.strip()

            if refinement.startswith("{"):  # Check if the response includes a refined plan
                updated_plan = validate_and_clean_json(refinement)
                if updated_plan:
                    response_data.update({
                        "plan": updated_plan,
                        "summary": summarize_plan(updated_plan),
                        "response": f"Plan updated based on your input: '{user_query}'."
                    })
                else:
                    response_data["response"] = "Failed to refine the existing plan."
            else:
                # Retain the existing plan and provide a response
                response_data.update({
                    "response": refinement,
                    "plan": current_plan,  # Explicitly retain the current plan
                    "summary": current_summary  # Keep the existing summary
                })

        else:
            # Case 3: Irrelevant or general conversational input
            general_prompt = (
                "You are a helpful assistant specializing in general conversational responses. "
                "The user's input is unrelated to learning plans or the knowledge base. "
                "Respond politely and professionally, focusing on the role of a data science assistant."
            )
            general_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": general_prompt},
                    {"role": "user", "content": user_query},
                ],
            )
            response_data.update({
                "response": general_response.choices[0].message.content.strip(),
                "plan": current_plan,  # Explicitly retain the current plan
                "summary": current_summary  # Keep the existing summary
            })

    except Exception as e:
        response_data["response"] = "An error occurred while processing your query. Please try again later."

    return response_data

@app.post("/save_plan")
async def save_plan(request: dict, username: str = Depends(get_current_username)):
    """
    Save the learning plan and module details to Snowflake.
    """
    plan = request.get("plan")
    summary = request.get("summary")

    # Debug: Log the incoming request
    logging.info(f"Received save_plan request: Plan: {plan}, Summary: {summary}")

    if not plan or not summary:
        raise HTTPException(status_code=400, detail="Plan and summary are required.")

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Insert plan into the database
            plan_id = plan.get("PlanID", str(datetime.utcnow().timestamp()))
            title = plan.get("Title", "Untitled Plan")
            key_topics = json.dumps(plan.get("KeyTopics", []))
            learning_outcomes = plan.get("ExpectedOutcome", "N/A")

            # Debug: Log the plan being inserted
            logging.info(f"Inserting Plan: ID: {plan_id}, Title: {title}, User: {username}")

            cursor.execute(
                """
                INSERT INTO PLANS (PLAN_ID, USERNAME, TITLE, SUMMARY, KEY_TOPICS, LEARNING_OUTCOMES)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (plan_id, username, title, summary, key_topics, learning_outcomes)
            )

            # Insert module details
            for module in plan.get("Modules", []):
                module_id = module.get("ModuleID", str(datetime.utcnow().timestamp()))
                module_number = module.get("module", 0)
                module_title = module.get("title", "No Title")
                description = module.get("description", "No Description")
                logging.info(f"Inserting Module: ID: {module_id}, Title: {module_title}, Plan ID: {plan_id}")

                cursor.execute(
                    """
                    INSERT INTO MODULES (MODULE_ID, PLAN_ID, MODULE, TITLE, DESCRIPTION)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (module_id, plan_id, module_number, module_title, description)
                )

            connection.commit()
            logging.info(f"Plan and modules saved successfully. Plan ID: {plan_id}")
            return {"message": "Plan saved successfully.", "plan_id": plan_id}
    except Exception as e:
        connection.rollback()
        logging.error(f"Error saving plan: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while saving the plan.")
    finally:
        connection.close()

@app.get("/get_plans")
def get_plans(username: str = Depends(get_current_username), page: int = 1, size: Optional[int] = 0):
    """
    Fetch paginated or all plans for the currently logged-in user.
    Set size=0 or size=None to fetch all results.
    """
    connection = get_db_connection()
    try:
        # Determine the offset and limit based on size
        offset = (page - 1) * size if size else 0  # Offset is zero if fetching all
        query = """
            SELECT plan_id, title, summary, key_topics, learning_outcomes
            FROM plans
            WHERE username = %s
        """
        if size:
            query += " LIMIT %s OFFSET %s"

        with connection.cursor() as cursor:
            if size:
                cursor.execute(query, (username, size, offset))
            else:
                cursor.execute(query, (username,))

            plans = [
                {
                    "plan_id": row[0],
                    "title": row[1],
                    "summary": row[2],
                    "key_topics": json.loads(row[3]) if row[3] else [],
                    "learning_outcomes": row[4],
                }
                for row in cursor.fetchall()
            ]

            if not plans:
                return {"message": "No plans available"}

            return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch plans")
    finally:
        connection.close()


@app.get("/get_modules/{plan_id}")
def get_modules(plan_id: str, page: int = 1, size: int = 10):
    connection = get_db_connection()
    try:
        offset = (page - 1) * size
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT MODULE_ID, PLAN_ID, MODULE, TITLE, DESCRIPTION
                FROM MODULES
                WHERE PLAN_ID = %s
                LIMIT %s OFFSET %s
                """,
                (plan_id, size, offset)
            )
            modules = cursor.fetchall()

            if not modules:
                return {"message": f"No modules available for plan ID: {plan_id}"}

            return [
                {
                    "module_id": row[0],
                    "plan_id": row[1],
                    "module": row[2],
                    "title": row[3],
                    "description": row[4],
                }
                for row in modules
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch modules")
    finally:
        connection.close()

@app.get("/get_module_details/{module_id}")
def get_module_details(module_id: str):
    """
    Fetch module details and generate a structured, article-like detailed explanation dynamically.
    """
    connection = get_db_connection()
    try:
        # Step 1: Retrieve module details from the database
        cursor = connection.cursor()
        cursor.execute(
            "SELECT MODULE_ID, MODULE, TITLE, DESCRIPTION FROM MODULES WHERE MODULE_ID = %s",
            (module_id,)
        )
        module = cursor.fetchone()
        if not module:
            return {"message": f"No details found for module ID: {module_id}"}

        title, description = module[2], module[3]  # Extract title and description

        # Step 2: Retrieve raw explanation from Pinecone
        raw_explanation = retrieve_detailed_explanation(title, description, top_k=30)

        # Step 3: Use OpenAI to format the explanation into an article
        try:
            
            system_prompt = f"""
                You are an AI assistant tasked with synthesizing a detailed and professional article based on the provided explanation text.
                The explanations are curated to include highly relevant information (relevance score > 0.85) and represent key insights about the topic.
 
                **Context**:
                - Module Title: {title}
                - Module Description: {description}
 
                **Purpose**:
                Your goal is to generate a comprehensive and insightful article that educates readers on the topic.
                The article should be structured naturally and cohesively, presenting the information in a logical and engaging manner.
 
                **Content Guidelines**:
                1. Use all the provided explanation text, ensuring the original meaning and context are retained.
                2. Highlight key points and elaborate where necessary to ensure clarity and understanding.
                3. Include relevant Python code snippets and formulas to enhance the explanation. For instance:
                    - If the topic involves concepts like linear regression, present the formula \( y = mx + c \), explain each component (e.g., \( y \) is the target variable, \( m \) is the slope, \( x \) is the input feature, and \( c \) is the intercept), and provide Python code snippets such as:
                    ```python
                    # Example: Linear regression implementation
                    from sklearn.linear_model import LinearRegression
 
                    # Data
                    X = [[1], [2], [3]]
                    y = [2, 4, 6]
 
                    # Model training
                    model = LinearRegression()
                    model.fit(X, y)
 
                    # Making predictions
                    predictions = model.predict([[4]])
                    print(predictions)
                    ```
                    - Include code snippets wherever relevant information is being generated or derived, and explain how the code interacts with the formula, breaking down its components.
                    - Code snippets should not be restricted to specific topics like linear regression but should be included wherever necessary to illustrate concepts effectively and provide practical context.
                4. Ensure the code snippets and formulas are properly formatted, seamlessly integrated, and relevant to the explanation. Avoid overloading the article with unnecessary technical content. Focus on clarity and context.
                5. Do not introduce any extra context accept the one user has provided you with.
 
                **Style**:
                - Write in a professional and engaging tone suitable for an educational audience.
                - Organize the content in a manner that flows logically, allowing readers to follow the topic easily.
                - Use paragraphs, headings, or bullet points where necessary to improve readability.
                - Ensure smooth transitions between ideas and sections for coherence.
 
                **Additional Instructions**:
                - Focus on clarity, coherence, and logical progression of ideas.
                - Avoid unnecessary repetition and ensure the article stays on topic.
                - don't hallucinate, don't bullshit, have concrete answers. NO ifs, maybes
 
                **Provided Explanation Text**:
                {raw_explanation}
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}],
                max_tokens=1000,
                temperature=0
            )
            formatted_explanation = response.choices[0].message.content.strip()

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error formatting explanation: {str(e)}")

        # Step 4: Return module details with formatted explanation
        return {
            "module_id": module[0],
            "module": module[1],
            "title": title,
            "description": description,
            "detailed_explanation": formatted_explanation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch module details")
    finally:
        cursor.close()
        connection.close()

@app.get("/get_relevant_youtube_video/{module_id}", response_model=YouTubeVideoResponse)
async def get_relevant_youtube_video(module_id: str, cached_data: dict = Depends(get_module_details)):

    try:
        logger.info("Fetching relevant YouTube video for module ID: %s", module_id)

        module_title = cached_data["title"]
        module_description = cached_data["description"]
        module_detailed_explanation = cached_data["detailed_explanation"]


        module_title = cached_data["title"]
        module_description = cached_data["description"]
        module_detailed_explanation = cached_data["detailed_explanation"]

        combined_text = f"{module_title} {module_description} {module_detailed_explanation}"

        # Step 1: Summarize input text
        summarized_text = summarize_text(combined_text)

        # Step 2: Fetch YouTube videos
        videos = fetch_youtube_videos(summarized_text)
        if not videos:
            logger.warning("No relevant YouTube videos found")
            raise HTTPException(status_code=404, detail="No relevant YouTube videos found.")

        # Step 3: Process transcripts and upsert to Pinecone
        for video in videos:
            transcript_text = fetch_video_transcript(video["video_id"])
            if transcript_text:
                transcript_chunks = chunk_text(transcript_text)
                upsert_to_pinecone(video["video_id"], video["title"], video["description"], transcript_chunks)

        # Step 4: Generate embedding for the module content
        module_embedding = generate_embedding(combined_text)

        # Step 5: Query Pinecone for the most relevant video
        search_results = youtube_index.query(vector=module_embedding, top_k=1, include_metadata=True)
        if not search_results["matches"]:
            logger.warning("No matches found in Pinecone")
            return {"video_url": None, "relevance_score": None}

        # Extract the most relevant match
        best_match = search_results["matches"][0]
        video_url = f"https://www.youtube.com/watch?v={best_match['metadata']['video_id']}"
        relevance_score = best_match["score"]
        transcript = fetch_video_transcript(best_match["metadata"]["video_id"]) or "Transcript unavailable."

        return {
            "video_url": video_url,
            "relevance_score": best_match["score"],
            "transcript": transcript
        }

        # return {"video_url": video_url, "relevance_score": relevance_score}
        transcript = fetch_video_transcript(best_match["metadata"]["video_id"]) or "Transcript unavailable."

        # return {
        #     "video_url": video_url,
        #     "relevance_score": best_match["score"],
        #     "transcript": transcript
        # }

        # return {"video_url": video_url, "relevance_score": relevance_score}

    except Exception as e:
        logger.error(f"Error in /get_relevant_youtube_video endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
ARXIV_API_URL = "http://export.arxiv.org/api/query"

@app.get("/get_relevant_arxiv_paper/{module_id}", response_model=List[ArxivPaperResponse])
async def get_relevant_arxiv_paper(module_id: str, cached_data: dict = Depends(get_module_details)):
    try:
        logger.info("Fetching relevant Arxiv papers for module ID: %s", module_id)

        # Extract module details from cached data
        module_title = cached_data["title"]
        module_description = cached_data["description"]
        module_detailed_explanation = cached_data["detailed_explanation"]

        combined_text = f"{module_title} {module_description} {module_detailed_explanation}"

        # Step 1: Summarize input text
        summarized_text = summarize_text_arxiv(combined_text)

        # Step 2: Fetch papers from Arxiv API
        params = {
            "search_query": f"all:{summarized_text}",
            "start": 0,
            "max_results": 2,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        response = requests.get(ARXIV_API_URL, params=params)

        if response.status_code != 200:
            logger.warning("Failed to fetch data from Arxiv. Status code: %d", response.status_code)
            raise HTTPException(status_code=500, detail="Failed to fetch data from Arxiv.")

        # Parse the XML response
        data = xmltodict.parse(response.text)
        entries = data.get('feed', {}).get('entry', [])

        # If a single entry, convert to list for uniform processing
        if isinstance(entries, dict):
            entries = [entries]

        # Step 3: Process entries
        results = []
        for entry in entries:
            authors = entry.get('author', [])
            if isinstance(authors, dict):
                authors = [authors]
            author_names = [author.get('name', '') for author in authors]

            # Summarize paper summary
            paper_summary = entry.get('summary', '').replace('\n', ' ').strip()
            summarized_paper_summary = summarize_text(paper_summary) if paper_summary else "Summary unavailable."

            paper = {
                "title": entry.get('title', '').replace('\n', ' ').strip(),
                "summary": summarized_paper_summary,
                "authors": author_names,
                "published": entry.get('published', ''),
                "link": entry.get('id', ''),
                "pdf_url": next((
                    link.get('@href', '') for link in entry.get('link', [])
                    if isinstance(link, dict) and link.get('@title') == 'pdf'
                ), None)
            }
            results.append(paper)

        if not results:
            logger.warning("No relevant papers found for query: %s", summarized_text)
            raise HTTPException(status_code=404, detail="No relevant papers found.")

        return results

    except Exception as e:
        logger.error(f"Error in /get_relevant_arxiv_paper endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

logging.basicConfig(level=logging.DEBUG)  # Set the level to DEBUG or INFO
logger = logging.getLogger(__name__)

# @app.get("/get_image_urls_with_summaries/{module_id}")
# def get_image_urls_with_summaries(module_id: str):
#     """
#     Retrieve image URLs based on the module ID and generate summaries for the images using OpenAI.
#     """
#     logging.info(f"Received request to fetch image URLs and summaries for module_id: {module_id}")
#     connection = get_db_connection()
#     try:
#         # Step 1: Retrieve module details from the database
#         logging.info("Attempting to fetch module details from the database.")
#         cursor = connection.cursor()
#         cursor.execute(
#             "SELECT MODULE_ID, MODULE, TITLE, DESCRIPTION FROM MODULES WHERE MODULE_ID = %s",
#             (module_id,)
#         )
#         module = cursor.fetchone()
 
#         if not module:
#             logging.warning(f"No module details found for module_id: {module_id}")
#             return {"message": f"No details found for module ID: {module_id}"}
 
#         logging.info(f"Module details retrieved successfully: {module}")
#         title, description = module[2], module[3]
 
#         # Step 2: Construct query text using title
#         model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
#         processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
#         query_text = f"{title}"
#         query_embedding = generate_text_embedding(query_text, model, processor)
#         logging.info(f"Constructed query text for embedding: {query_embedding}")
 
#         # Step 3: Retrieve image URLs from Pinecone
#         logging.info("Querying Pinecone for image URLs.")
#         results = image_index.query(
#             vector=query_embedding.tolist(),
#             top_k=1,
#             include_metadata=True
#         )
 
#         # Extract URLs from the results
#         urls = [result['metadata']['url'] for result in results['matches'] if 'url' in result['metadata']]
 
#         # Step 4: Summarize images using OpenAI
#         summaries = []
#         for url in urls:
#             try:
#                 # Summarize the image directly using OpenAI
#                 logging.info(f"Summarizing image at URL: {url}")

#                 response = client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {"role": "system", "content": "You are an assistant that summarizes images and make sure to summarize it in short. Summarize the image relating it to the query text provided."},
#                         {"role": "user", "content": f"Summarize the content of this image: {url} {query_text}"}
#                     ]
#                 )
#                 summary = response.choices[0].message.content.strip()
#                 # summary = response['choices'][0]['message']['content']
#                 logging.info(f"Generated summary: {summary}")
#             except Exception as e:
#                 logging.error(f"Error summarizing image {url}: {e}")
#                 summary = "Unable to summarize image."
#             summaries.append({"url": url, "summary": summary})
 
#         # Step 5: Format and return the response
#         if not summaries:
#             logging.info("No matching images found in Pinecone.")
#             return {
#                 "module_id": module_id,
#                 "module": module[1],
#                 "title": title,
#                 "description": description,
#                 "images": [],
#                 "message": "No matching images found."
#             }
 
#         logging.info("Image URLs and summaries fetched successfully. Preparing response.")
#         return {
#             "module_id": module_id,
#             "module": module[1],
#             "title": title,
#             "description": description,
#             "images": summaries
#         }
 
#     except Exception as e:
#         logging.error(f"Error processing module ID {module_id}: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Error processing module ID: {str(e)}")
#     finally:
#         logging.info("Closing database connection.")
#         cursor.close()
#         connection.close()
  
   

@app.get("/generate_flashcards/{module_id}", response_model=FlashcardGeneration)
async def generate_flashcards(
    module_id: str, 
    cached_data: dict = Depends(get_module_details),
    youtube_data: dict = Depends(get_relevant_youtube_video)
):
    
    try:
        logger.info("Generating flashcards for module ID: %s", module_id)
        
        module_detailed_explanation = cached_data["detailed_explanation"]

        transcript = youtube_data.get("transcript", "")

        context = (
            "You are an expert summarizer and your job is to summarize the below data in 5-6 sentences."
            f"Detailed Explanation: {module_detailed_explanation}\n"
            f"Relevant YouTube Transcript: {transcript}\n\n"
        )

        system_prompt = (
            "You are an educational assistant. Based on the provided context, "
            "create concise flashcards. Each flashcard should have a 'question' and an 'answer' "
            "that are directly relevant to the context. Output the flashcards in a JSON-like format, "
            "with each flashcard being a nested object with 'question' and 'answer' keys. Strictly return "
            "a valid JSON output only. Do not include any introductory text, explanations, or comments. "
            "The response should look like this:\n"
            "[\n"
            "  {\"question\": \"What is question 1?\", \"answer\": \"Answer to question 1.\"},\n"
            "  {\"question\": \"What is question 2?\", \"answer\": \"Answer to question 2.\"},\n"
            "  ...\n"
            "]"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ],
            max_tokens=500,
        )

        flashcards_text = response.choices[0].message.content.strip()

        # Parse the JSON-like response into nested question-answer objects

        import json
        flashcards = []
        try:

            flashcards = json.loads(flashcards_text)  # Parse JSON-like response
            logger.debug("Successfully parsed JSON response for flashcards.")

        except json.JSONDecodeError:

            logger.warning("Response not in JSON format; attempting manual parsing.")
            lines = flashcards_text.split("\n")
            
            for i in range(0, len(lines), 2):

                question = lines[i].strip()
                answer = lines[i + 1].strip() if i + 1 < len(lines) else ""
                flashcards.append({"question": question, "answer": answer})

        for idx, flashcard in enumerate(flashcards):

            logger.debug("Flashcard %d: Question: %s, Answer: %s", idx + 1, flashcard.get("question"), flashcard.get("answer"))

        # Return the flashcards wrapped in FlashcardGeneration model

        return FlashcardGeneration(flashcards=flashcards)

    except Exception as e:

        logger.error(f"Error in /generate_flashcards endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/generate_quiz/{module_id}", response_model=QuizGeneration)
async def generate_quiz(
    module_id: str,
    cached_data: dict = Depends(get_module_details),
    youtube_data: dict = Depends(get_relevant_youtube_video)
):
    try:
        logger.info("Generating quiz for module ID: %s", module_id)

        # Extract module details and YouTube transcript
        module_detailed_explanation = cached_data["detailed_explanation"]
        transcript = youtube_data.get("transcript", "")

        # Combine context for quiz generation
        context = (
            f"Detailed Explanation: {module_detailed_explanation}\n"
            f"Relevant YouTube Transcript: {transcript}\n\n"
        )

        system_prompt = (
            "You are an educational assistant. Based on the provided context, "
            "create a quiz with 5 multiple-choice questions. Each question should have "
            "four answer options, and one should be the correct answer. Output the quiz "
            "in a JSON format with each question as an object containing 'question', 'options', "
            "and 'correct_answer' keys. Strictly return a valid JSON output only. Do not include "
            "any introductory text, explanations, or comments. The response should look like this:\n"
            "[\n"
            "  {\"question\": \"What is question 1?\", \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"], \"correct_answer\": \"Option A\"},\n"
            "  {\"question\": \"What is question 2?\", \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"], \"correct_answer\": \"Option B\"},\n"
            "  ...\n"
            "]"
        )

        # Generate quiz via OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ],
            max_tokens=750,
        )

        quiz_text = response.choices[0].message.content.strip()

        # Parse the JSON-like response into question-answer objects
        import json
        quiz = []
        try:
            quiz = json.loads(quiz_text)  # Parse JSON-like response
            logger.debug("Successfully parsed JSON response for quiz.")
        except json.JSONDecodeError:
            logger.warning("Response not in JSON format; attempting manual parsing.")

        # Log the generated questions for debugging
        for idx, question in enumerate(quiz):
            logger.debug(
                "Question %d: %s", idx + 1, question.get("question")
            )

        # Return the quiz wrapped in QuizGeneration model
        return QuizGeneration(quiz=quiz)

    except Exception as e:
        logger.error(f"Error in /generate_quiz endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    return response

@app.on_event("shutdown")
async def close_connection_pool():
    pool.close_all_connections()