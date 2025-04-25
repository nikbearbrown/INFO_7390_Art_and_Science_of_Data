import streamlit as st
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader

from chains import Chain
from utils import clean_text, validate_url

def create_streamlit_app(llm, clean_text):
    st.title("🧑‍💻 Coverly: Your Job Specific AI Cover Letter Generator")
    url_input = st.text_input("Enter job posting URL:", placeholder="e.g. https://careers.coca-colacompany.com/job/20698954/data-scientist-ai-ml-sofia-bg/")
    pdf_input = st.file_uploader('Choose your Resume (in .pdf format):', type="pdf")
    if pdf_input:
        temp_file = r"tmp/temp.pdf"
        with open(temp_file, "wb") as file:
            file.write(pdf_input.getvalue())

    submit_button = st.button("Submit")

    if submit_button:
    # st.code("Hello World", language='markdown')
        # Validate the URL
        if not validate_url(url_input):
            st.error("Invalid URL")

        if url_input and pdf_input:
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                jobs = llm.extract_jobs(data)
                for job in jobs:
                    cv_loader=PyPDFLoader(temp_file)
                    cv_docs=cv_loader.load()[0].page_content
                    cv_data=clean_text(cv_docs)
                    cv,cv_rm = llm.write_cv(job, cv_data)
                    st.code(body=cv, language='markdown')
                    op=f"""Token Information:  
                    Output Tokens = {cv_rm['token_usage']['completion_tokens']}  
                    Total Time = {cv_rm['token_usage']['total_time']:.2f} sec  
                    Model Name = {cv_rm['model_name']}  
                    """
                    st.info(op, icon="ℹ️")

            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        else:
            st.error("Job posting URL or Resume pdf is missing.")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="AI Cover Letter Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)
