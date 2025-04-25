import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_cv(self, job, cv):
        prompt_cv = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
            Write a cover letter based for above mentioned job description based on following resume {cv}
            Also, include relevant projects of resume if they match requirement of job description.
            Do not provide a preamble.
            ### COVER LETTER (NO PREAMBLE):        
            """
            )

        chain_email = prompt_cv | self.llm
        res_cv = chain_email.invoke({"job_description": str(job), "cv": cv})
        
        try:
            res_cv_op = res_cv.content
            res_cv_rm = res_cv.response_metadata
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res_cv_op,res_cv_rm
        # if isinstance(res_cv_op, list) else [res_cv_op]

# if __name__ == "__main__":
#     print(os.getenv("GROQ_API_KEY"))
