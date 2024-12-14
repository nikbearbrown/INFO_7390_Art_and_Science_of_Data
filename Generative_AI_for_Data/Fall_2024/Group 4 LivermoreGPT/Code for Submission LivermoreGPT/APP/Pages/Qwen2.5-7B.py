import streamlit as st
import PageTemplate.ChatPageTemplate as ChatPageTemplate
import ollama
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from streamlit import subheader

from Utilities.LoadData import load_doc, load_local_index, load_sentence_transformer_model

with st.spinner("Loading LivermoreGPT with Qwen2.5:7b via Ollama..."):
    load_doc()
    load_sentence_transformer_model()
    load_local_index()


def chatFunction():
    theQuestion = st.session_state.messages[-1]["content"]
    theQuestion_embedding = load_sentence_transformer_model().encode([theQuestion])

    # Retrieve top k most similar questions
    top_k = 5
    k = min(top_k, len(load_doc()))
    D, I = load_local_index().search(theQuestion_embedding, k)
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
        Question:
        \"\"\"
        {theQuestion}
        \"\"\"
    '''
    theMessage = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

    theMessage[-1]["content"] = prompt
    theMessage.insert(-2, {"role": "system", "content": bio})
    # print(theMessage)
    # st.write(theMessage)


    stream = ollama.chat(
        model='Qwen2.5:7b',
        messages= theMessage,
        stream=True,
    )

    def wrapper_stream(stream):
        for message in stream:
            yield message['message']['content']

    return wrapper_stream(stream)

ChatPageTemplate.ChatPageTemplate(
    subHeader="LivermoreGPT with Qwen2.5:7b via Ollama",
    chatFunction=chatFunction,
    streamSupported=True
)
