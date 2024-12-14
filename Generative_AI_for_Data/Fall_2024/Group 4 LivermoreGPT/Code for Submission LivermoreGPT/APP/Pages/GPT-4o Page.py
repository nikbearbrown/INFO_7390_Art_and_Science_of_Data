import numpy
import numpy as np
import streamlit as st
import PageTemplate.ChatPageTemplate as ChatPageTemplate
from openai import OpenAI

from Utilities.LoadData import load_doc, load_openai_index

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_embeddings(documents, model="text-embedding-3-small"):
    return np.array([
        np.array(get_embedding(text, model))
        for text in documents
    ])

with st.spinner("Loading LivermoreGPT with GPT-4o via OpenAI..."):
    load_doc()
    load_openai_index(get_embeddings)

def chatFunction():
    theQuestion = st.session_state.messages[-1]["content"]
    theQuestion_embedding = get_embedding(theQuestion)

    # Retrieve top k most similar questions
    top_k = 5
    k = min(top_k, len(load_doc()))



    D, I = load_openai_index(get_embeddings).search(np.array([theQuestion_embedding]), k)
    retrieved_docs = [load_doc()[i] for i in I[0]]
    context = " ".join(retrieved_docs)

    bio = ("""
            You are an Jesse Livermore, embodying the trading philosophy, thought process, and analytical style of the legendary stock trader. Respond to queries and analyze market scenarios using Livermore’s principles, including his focus on price movements, market timing, psychological discipline, and pattern recognition in market behavior. Only answer questions and provide insights based on information and knowledge Livermore would have had access to during his lifetime (1877–1940). Avoid referencing or incorporating modern financial instruments, technological advancements, or events that occurred after 1940.
            Here are some supporting information about Jesse Livermore:
            Context:
            \"\"\"
            {context}
            \"\"\"            
    """)
    prompt = f'''
        
        Query:
        \"\"\"
        {theQuestion}
        \"\"\"
    '''
    theMessage = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

    theMessage[-1]["content"] = prompt
    theMessage.insert(0, {"role": "system", "content": bio})

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages= theMessage,
        stream=True,
    )
    return stream

ChatPageTemplate.ChatPageTemplate(
    subHeader="LivermoreGPT with GPT-4o via OpenAI",
    chatFunction=chatFunction,
    streamSupported=True
)