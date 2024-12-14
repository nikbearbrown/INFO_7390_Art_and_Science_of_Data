from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.retrievers import ArxivRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, chain
from langchain_core.tools import tool

from serpapi import GoogleSearch
import os

from fast_api.langgraph_api.config import SERPAPI_PARAMS, OPENAI_API_KEY

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@tool("fetch_arxiv")
def fetch_arxiv(query: str):
    """Perform retrieval from Arxiv website and get a response from a retriever."""
    retriever = ArxivRetriever(
    load_max_docs=3,
    get_ful_documents=True,
    )
 
    prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.
 
    Context: {context}
 
    Question: {question}"""
    )
 
    llm = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
 
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
 
    response = chain.invoke(query)
    
    return response

@tool("rag_search")
def rag_search(query: str, index_name: str):
    """Perform RAG operation and get a response from an agent."""
    print("---CALL REACT AGENT---")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    index_name="advdatascience"

    vectorstore = PineconeVectorStore(index_name=index_name,
                                                pinecone_api_key=pinecone_api_key,
                                                embedding=embeddings)


    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

    prompt = ChatPromptTemplate.from_template("""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
            
Question: {question} 

Context: {context} 

Answer:"""
)

    llm = ChatOpenAI(temperature=0, streaming=True, model="gpt-4o-mini", api_key=OPENAI_API_KEY)

    @chain
    def run_retriever(input_):
        """Run the retriever to get the relevant documents."""
        docs = retriever.invoke(input_["question"])
        return format_docs(docs)
    
    rag_chain = RunnablePassthrough.assign(context=run_retriever) | prompt | llm | StrOutputParser()

#     rag_chain = RunnableParallel({
#     "context": retriever | format_docs,
#     "question": RunnablePassthrough(),
#     "index_name": RunnablePassthrough(),
# }) | prompt | llm | StrOutputParser()

    # rag_chain = (
    #     {"context": retriever | format_docs, "question": RunnablePassthrough(), "index_name": RunnablePassthrough()}
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )

    response = rag_chain.invoke({"question": query, "index_name": index_name})

    return response

@tool("web_search")
def web_search(query: str):
    """Finds general knowledge information using Google search. Can also be used
    to augment more 'general' knowledge to a previous specialist query."""
    search = GoogleSearch({
        **SERPAPI_PARAMS,
        "q": query,
        "num": 5
    })
    results = search.get_dict()["organic_results"]
    contexts = "\n---\n".join(
        ["\n".join([x["title"], x["snippet"], x["link"]]) for x in results]
    )

    print(contexts)
    
    return contexts

@tool("final_answer")
def final_answer(
    introduction: str,
    research_steps: str,
    main_body: str,
    exhibits: str,
    conclusion: str,
    sources: str
):
    """Returns a natural language response to the user in the form of a research
    report. There are several sections to this report, those are:
    - `introduction`: a short paragraph introducing the user's question and the
    topic we are researching.
    - `research_steps`: a few bullet points explaining the steps that were taken
    to research your report.
    - `main_body`: this is where the bulk of high quality and concise
    information that answers the user's question belongs. It is 3-4 paragraphs
    long in length.
    - `exhibits`: this is where links to the images are provided along with
    a one sentence description of the image.
    - `conclusion`: this is a short single paragraph conclusion providing a
    concise but sophisticated view on what was found.
    - `sources`: a bulletpoint list of sources enclosed in brackets '[]' along 
    with urls enclosed in parentheses '()' detailing sources for all information 
    referenced during the research process. Example: [Source](https://example.com)
    """
    if type(research_steps) is list:
        research_steps = "\n".join([f"- {r}" for r in research_steps])
    if type(sources) is list:
        sources = "\n".join([f"- {s}" for s in sources])
    return ""