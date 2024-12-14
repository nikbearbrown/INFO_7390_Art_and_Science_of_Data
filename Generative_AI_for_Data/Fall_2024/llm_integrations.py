import google.generativeai as genai


from dotenv import load_dotenv

import os
load_dotenv()


# Initialize Gemini LLM
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_response_from_llm(prompt):

    try:
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate content
        response = model.generate_content(prompt)

        # Debugging: Print raw response
        print("LLM Response:", response)

        # Extract and return the text response
        if response and response.candidates:
            # Access the text from the first candidate
            first_candidate = response.candidates[0]
            if hasattr(first_candidate.content, "parts") and first_candidate.content.parts:
                return first_candidate.content.parts[0].text.strip()
            else:
                return "Sorry, I couldn't extract the response content."
        else:
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error generating response: {str(e)}"



