import streamlit as st
import pandas as pd
from bot_response import fetch_from_pinecone, generate_response

def match_skills_to_courses(skills, courses_df):
    matching_courses = []
    for index, row in courses_df.iterrows():
        if any(skill.lower() in row['Course Description'].lower() for skill in skills):
            matching_courses.append(row)
    return pd.DataFrame(matching_courses)

def split_instructors(instructors_string):
    return [name.strip() for name in instructors_string.split(',')]


def handle_message():
    user_message = st.session_state.user_message.strip()
    if user_message:
        # Add user's message to session
        st.session_state.messages.append(
            {"role": "user", "content": user_message})
        # Generate GPT response
        response = generate_response(user_message, "")
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        # Clear input box
        st.session_state.user_message = ""

# Set up Streamlit page
st.set_page_config(page_title="NEU Course Recommendation System", layout="wide")

# Load the Northeastern University logo
logo_path = "Northeastern-University-Logo.png"
file_path = "./output/ExtractedCourseDescriptions.csv"  # Update the path as needed
course_data = pd.read_csv(file_path)

# Apply custom CSS for enhanced visuals and chat ribbon
st.markdown(
    """
    <style>
    /* Page background and main text */
    .main {background-color: #f1f1f1; color: #2c3e50; font-family: 'Helvetica Neue', sans-serif;}

    /* Header and title styles */
    h1 {
        color: #cc0000;
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 10px;
    }

    h3 {
        color: #2c3e50;
        font-weight: 600;
        text-align: center;
        font-size: 24px;
    }

    h4 {
        color: #7f8c8d;
        text-align: center;
        font-size: 18px;
    }

    /* Sidebar styles */
    .stSidebar {
        background-color: #34495e;
        color: white;
        border-radius: 10px;
        padding: 20px;
    }

    .stSidebar h3, .stSidebar label, .stSidebar p {
        color: white;
        font-weight: 500;
    }

    .stButton>button {
        background-color: #cc0000;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #e74c3c;
        transition: 0.3s;
    }

    /* Course card design */
    .card {
        background-color: #ffffff;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s;
        overflow: hidden; /* Ensure content stays inside */
        word-wrap: break-word; /* Break long words */
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .card strong {
        color: #cc0000;
        font-weight: 600;
    }

    .card table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }

    .card th, .card td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
        word-wrap: break-word; /* Break long text */
        overflow: hidden; /* Prevent overflow */
    }

    .card th {
        background-color: #f2f2f2;
    }

    /* Footer style */
    .footer {
        background-color: #2c3e50;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 14px;
        margin-top: 40px;
        z-index: 1000;
    }

    /* Chat ribbon styles */
    .chat-ribbon {
        position: fixed;
        bottom: 10px;
        right: 20px;
        background-color: #cc0000;
        color: white;
        padding: 15px 20px;
        border-radius: 30px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        font-size: 18px;
        cursor: pointer;
        z-index: 999;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header with logo and title
st.image(logo_path, width=250)
st.title("📘 Northeastern University Course Recommendation System")
st.markdown("<h3>Discover the perfect courses to match your skills and interests! </h3>", unsafe_allow_html=True)

# Skills list for user to select
skills_list = [
"Python", "Java", "Data Science", "Machine Learning", "Networking", "Web Development", "Cloud Computing", "SQL",
"Linux", "Kubernetes", "Scala", "Pthreads", "Chef", "Puppet", "Ansible", "Salt", "Containers", "Virtual Machines", 
"Microservices", "REST", "AJAX", "TensorFlow", "Pytorch", "GAN", "Bayesian Networks", "NLP", "CNN", "Hadoop", 
"MongoDB", "NoSQL", "Data Warehousing", "PL/SQL", "R", "Blockchain", "Cryptocurrency", "Smart Contracts", 
"Deep Learning", "React", "Angular", "Node.js", "Express.js", "Docker", "Git", "Jenkins", "CI/CD", "GitHub Actions",
"AWS", "Azure", "Google Cloud Platform", "BigQuery", "Data Science Pipelines", "Tableau", "Power BI", "JavaScript", 
"HTML", "CSS", "GraphQL", "Vue.js", "Redux", "TypeScript", "Swift", "Objective-C", "Ruby", "PHP", "Perl", "Shell Scripting", 
"Bash", "PowerShell", "F#", "Clojure", "Rust", "Go", "Kotlin", "C++", "Visual Studio", "Eclipse", "IntelliJ IDEA", 
"Jupyter", "Sublime Text", "Atom", "Xcode", "MATLAB", "MongoDB Atlas", "DynamoDB", "Redis", "Elasticsearch", "Firebase", 
"PostgreSQL", "MySQL", "SQLite", "AWS Lambda", "AWS EC2", "AWS S3", "Google Firebase", "Google Bigtable", "App Engine", 
"Microsoft SQL Server", "Cassandra", "Snowflake", "Cloudera", "Apache Spark", "HBase", "Apache Kafka", "Apache Flink", 
"Terraform", "Docker Swarm", "Jenkins Pipeline", "Prometheus", "Grafana", "HashiCorp Vault", "Azure DevOps", "GitOps", "Helm", 
"CloudFormation", "CloudWatch", "CloudTrail", "Bitbucket", "GitLab", "CircleCI", "Travis CI", "Kubernetes Operators", 
"Jenkins X", "SonarQube", "Nagios", "AppDynamics", "New Relic", "Datadog", "Sentry", "Splunk", "Wireshark", "Metasploit", 
"Nmap", "Kali Linux", "Ethical Hacking", "Penetration Testing", "Load Balancer", "Reverse Proxy", "OAuth", "JWT", "OpenID Connect", 
"WebSockets", "OAuth2", "JWT", "Serverless", "Microservices Architecture", "Event-Driven Architecture", "CI/CD Pipeline", 
"Automated Testing", "Test-Driven Development", "Behavior-Driven Development", "Cloud-Native", "DevOps Automation", 
"Serverless Framework", "Xamarin", "React Native", "Flutter", "JavaFX", "Objective-C", "Rust", "Go", "Graph Databases", 
"Service Mesh", "Infrastructure as Code", "OpenShift", "Redshift", "Big Data", "CI/CD Automation", "Data Science Workflow", 
"Server-Side Rendering", "GraphQL Subscriptions", "Vuex", "Nuxt.js", "Sass", "LESS", "Tailwind CSS", "Babel", "Webpack", 
"Parcel", "Vite", "OpenAPI", "Swagger", "RESTful APIs", "Microservices Communication", "API Gateway", "gRPC", "Kong API Gateway", 
"API Rate Limiting", "Load Testing", "Performance Monitoring", "JMeter", "Gatling", "Cypress", "Selenium", "Jasmine", "Mocha", 
"Chai", "Jest", "Karma", "Enzyme", "Postman", "Swagger UI", "Mockito", "JUnit", "RSpec", "JUnit 5", "TestNG", "XUnit", 
"Zookeeper", "Kafka Connect", "Kafka Streams", "ETL", "Data Transformation", "Data Pipeline", "Data Modeling", "Dimensional Modeling", 
"OLAP", "ETL Process", "Data Integration", "Data Cleansing", "Data Mining", "Data Visualization", "Data Quality", "Big Data Analytics", 
"Data Architecture", "Data Governance", "Data Lineage", "Data Mesh", "Data Lakes", "Data Warehousing Design", "Data Auditing", 
"Data Provenance", "Data Privacy", "Data Security", "Encryption", "Decryption", "Access Control", "Identity Management", 
"Blockchain Security", "Cybersecurity", "Firewall", "SSL/TLS", "PKI", "Zero Trust Security", "SIEM", "Incident Response", 
"Security Orchestration Automation and Response", "Digital Forensics", "RPA", "AI in Cybersecurity", "Identity and Access Management", 
"Security Testing", "Vulnerability Scanning", "Penetration Testing", "Fuzz Testing", "Red Teaming", "Blue Teaming", "Incident Management"
]


# User selects skills
selected_skills = st.sidebar.multiselect(
    "Select Your Skills:",
    skills_list
)

# Chat functionality
if 'messages' not in st.session_state:
    st.session_state.messages = []


# Get course recommendations based on selected skills
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if st.sidebar.button("Get Recommendations"):
    if selected_skills:
        matches, markdown_result = fetch_from_pinecone(selected_skills)
        if markdown_result != "failed":
            st.session_state.recommendations = matches  # Save the matches for card rendering
        else:
            st.session_state.recommendations = None
            st.write("No recommendations found. Please try again.")
    else:
        st.write("Please select at least one skill.")


# Display recommendations as cards if they exist in the session state
if st.session_state.recommendations:
    # Display chat section
    st.markdown("<h3>Chat with CourseNavigator Bot</h3>", unsafe_allow_html=True)

    # Display chat messages dynamically
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"""
            <div style='text-align: right; margin: 10px;'>
                <div style='display: inline-block; background-color: #f1f1f1; color: #333333; padding: 10px;  border: 1px solid #d1d1d1; border-radius: 15px; max-width: 60%;'>
                    {message["content"]}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        elif message["role"] == "assistant":
            st.markdown(
                f"""
                <div style='text-align: left; margin: 10px;'>
                    <div style='display: inline-block; background-color: #f8d7da; padding: 10px; border-radius: 15px; max-width: 60%;'>
                        {message["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Input box for user to type their message
    st.text_input(
        "Type your message:",
        key="user_message",
        on_change=handle_message,
        placeholder="Ask about course details, timings, or more...",
    )
    
    for course in st.session_state.recommendations:
        metadata = course['metadata']
        course_id = metadata['Course ID']
        course_name = metadata['Course Name']
        score = round(course['score'] * 100, 2)

        markdown_output = []
        markdown_output.append(f"<h4>{course_id}: {course_name}</h4>")
        markdown_output.append(f"<p><strong>Score:</strong> {score}%</p>")
        markdown_output.append("<table>")
        markdown_output.append("<thead><tr><th>Instructor</th><th>Timings</th><th>CRN</th></tr></thead>")
        markdown_output.append("<tbody>")
        for instructor, timing, crn in zip(metadata['Instructors'], metadata['Timings'], metadata['CRNs']):
            markdown_output.append(f"<tr><td>{instructor}</td><td>{timing}</td><td>{crn}</td></tr>")
        markdown_output.append("</tbody></table>")

        markdown_result = "\n".join(markdown_output)

        # Display the card with the markdown table inside
        st.markdown(
            f"""
            <div class="card">
                {markdown_result}
            </div>
            """,
            unsafe_allow_html=True,
        )
    