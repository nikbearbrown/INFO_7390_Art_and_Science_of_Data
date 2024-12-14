from operator import index
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import streamlit as st

def load_doc():
    if "documents" not in st.session_state:
        file_path = './Data/reminiscences_of_a_stock_operator_qa.csv'
        data = pd.read_csv(file_path, sep='\t')

        file_path = "./Data/qna.csv"
        data2 = pd.read_csv(file_path, sep='\t')

        documents = np.concatenate(
            (np.array("Q: " + data['question'] + "\nA: " + data['answer']), np.array(data2['Question,Answer'])))

        st.session_state["documents"] = documents
        print("Documents loaded")

    return st.session_state["documents"]

def load_sentence_transformer_model():
    if "sentence_transformer_model" not in st.session_state:
        st.session_state["sentence_transformer_model"] = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2', device='cuda')
        print("Sentence Transformer Model loaded")
    return st.session_state["sentence_transformer_model"]

def load_openai_index(get_embeddings):
    if "openai_index" not in st.session_state:
        if not os.path.exists("./data/embeddings-openai.npy"):
            documents = load_doc()
            doc_embeddings = get_embeddings(documents)
            np.save("./data/embeddings-openai.npy", doc_embeddings)
        doc_embeddings = np.load("./data/embeddings-openai.npy")
        print("doc_embeddings loaded")



        index = faiss.IndexFlatL2(doc_embeddings.shape[1])
        index.add(doc_embeddings)


        st.session_state["openai_index"] = index

        print("OpenAI index loaded")

    return st.session_state["openai_index"]

def load_local_index():
    if "local_qwen_25_7b_index" not in st.session_state:
        if not os.path.exists("./data/embeddings-sentence-transformers-paraphrase-multilingual-mpnet-base-v2.npy"):
            model = load_sentence_transformer_model()
            documents = load_doc()
            doc_embeddings = model.encode(documents)
            np.save("./data/embeddings-sentence-transformers-paraphrase-multilingual-mpnet-base-v2.npy", doc_embeddings)
        doc_embeddings = np.load("./data/embeddings-sentence-transformers-paraphrase-multilingual-mpnet-base-v2.npy")
        print("doc_embeddings loaded")

        index = faiss.IndexFlatL2(doc_embeddings.shape[1])
        index.add(doc_embeddings)

        st.session_state["local_qwen_25_7b_index"] = index

        print("Qwen 2.5:7b index loaded")


    return st.session_state["local_qwen_25_7b_index"]

