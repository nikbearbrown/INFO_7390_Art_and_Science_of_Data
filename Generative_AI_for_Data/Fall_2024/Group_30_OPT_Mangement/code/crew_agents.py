from crewai import Agent, Crew, Task
from crewai_tools import  ScrapeWebsiteTool, SerperDevTool,WebsiteSearchTool
import os 
# Warning control
import warnings
warnings.filterwarnings('ignore')


openai_api_key = os.environ.get('OPENAI_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
# os.environ["SERPER_API_KEY"] = get_serper_api_key()
blog_url = "https://opt-imize.com/blog/"

search_optimize= WebsiteSearchTool(website_url=blog_url)
search_usics= WebsiteSearchTool(website_url="https://www.uscis.gov/working-in-the-united-states/")
search_ice= WebsiteSearchTool(website_url="https://www.ice.gov/sevis/schools#dhs-stem-designated-degree-program-list-and-cip-code-nomination-process")

global customer_name
customer_name = "jack"

#Agent1: rag reader
info_anlyst = Agent(
    role="Student lawful Info anlyst",
    goal="Discover all infomation regarding opt and student recuitment "
    "based on customer info",
    tools=[search_optimize, search_usics, search_ice],
    verbose=True,
    backstory=(
    "You're a reasoned lawyer with a knack for uncovering the latest terms and policy in opt and H1b."
    " Known for your ability to find the most relevant information and present it in a clear and concise manner."
    )
)


#Agent2: opt planer

opt_planer = Agent(
    role="student {visa_type} proccess customize planer",
    goal="Create detailed plan for customer based on customer info and student recuitment and opt info from info_anlyst",
    tools=[search_optimize, search_usics, search_ice],
    verbose=True,
    backstory=(
    "You're a lawyer planner that is Rigorous at creating detailed plans. You're known for your ability to create"
    " plans that are practical, and that meet the needs of the customer."
    )
)

#Agent3: opt plan qa
opt_plan_qa = Agent(
    role="opt or h1b plan QA anlyst",
    goal="Ensure the the quality of the plan and make sure it is based on customer info and {visa_type} info from info_anlyst",
    tools=[search_optimize, search_usics, search_ice],
    verbose=True,
    backstory=(
    "You're a meticulous analyst with a keen eye for detail."
    "You're known for your ability to ensure every plan is logistic and stick to the info related to {visa_type} and the customer inform"
    )
)


info_rag = Task(
    description="Conduct a thorough research about how to get {visa_type} for a {mayjor} student graduating in {grad_year}."
                "Make sure you find any relevant information given and present it in a clear and concise manner."
                "the current year is {current}.",
    expected_output=" A list with all relevant information.",
    agent=info_anlyst,
)


planing_task = Task(
    description="Review the context you got from the info analyst and create a detailed plan."
                "customer is graduating in {grad_year}, in {mayjor} and is looking to apply for {visa_type}."
                "customer name is {customer_name}."
                "Make sure the plan is detailed and based on all relevant information.",
    expected_output=" A fully fledge reports with the topic {visa_type}, each with a full section of information."
    "The report atleast contain sections for {visa_type} process, {visa_type} application, {visa_type} timeline, {visa_type} requirements."
    "The report should be clear and concise."
    "Formatted as markdown without '```'",
    agent=opt_planer,
    # async_execution=True,
    output_file="{customer_name}"+"_plan.md"
)

qa_task = Task(
    description="Review the plan created by the planer and make sure it is detailed and contains all relevant information."
                "    Make sure the plan is logistic and stick to the info related to opt and the customer information.",
    expected_output="Confirmation that the plan is detailed and contains all relevant information."
    "Confirmation that the plan is logistic and stick to the info related to opt and the customer information."
    "confirmation that the plan is formatted as markdown without '```'",
    agent=opt_plan_qa,
    async_execution=True,

)


opt_plan_crew = Crew(
    agents=[info_anlyst, 
            opt_planer, 
            opt_plan_qa],
    
    tasks=[info_rag, 
           qa_task, 
           planing_task],
    
    verbose=True
)


#get current year
import datetime
current_year = datetime.datetime.now().year



input_details = {
    'grad_year': "2024",
    'mayjor': "Computer Science",
    'visa_type': "opt",
    'customer_name': "jack",
    'current': str(current_year)
}

result = opt_plan_crew.kickoff(inputs=input_details)

print(result)