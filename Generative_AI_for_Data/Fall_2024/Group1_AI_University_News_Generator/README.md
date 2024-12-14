# *AI UNIVERSITY NEWS GENERATOR*

## *Detailed Documentation*: https://docs.google.com/document/d/1ysqY-ATauIbsHs9m6lmn6pXKRTC4hJPSRth4p02GDOc/edit?usp=sharing


## *Problem Statement*
Students struggle to stay informed on university updates due to fragmented and overwhelming information from diverse sources like social media and bulletins. A unified solution is needed to deliver concise, personalized, real-time news tailored to their interests, enhancing campus engagement and accessibility.

---

## *Background*
University campuses are dynamic environments where timely access to relevant updates is essential. Existing tools fail to offer a unified, personalized news delivery system tailored for university ecosystems. This project addresses this gap by leveraging AI technologies for efficient information aggregation and dissemination.

---

## *Retrieval-Augmented Generation (RAG) Implementation*
The *AI University News Generator* leverages Retrieval-Augmented Generation (RAG) to combine semantic search and generative AI for delivering highly relevant and personalized news updates.

### Key Components:
1. *Data Collection and Preprocessing*:
   - Aggregates data from multiple sources, including university websites, local news outlets, social media, and RSS feeds.
   - Uses tools like *Google Cloud Document AI* for document parsing and cleaning.
   - Preprocessed data is chunked into smaller segments for efficient indexing.

2. *Vector Database Integration*:
   - Converts preprocessed data into semantic embeddings using advanced LLMs (e.g., GPT-3.5/4).
   - Stores embeddings in a vector database such as *Milvus, **Pinecone, **Qdrant, or **Weaviate* for efficient retrieval.

3. *Query Processing*:
   - Processes user queries via LLMs to generate embeddings.
   - Embeddings are used to retrieve relevant information from the vector database.
   - Retrieved data is passed back to the LLM for content generation.

4. *News Generation*:
   - Combines retrieved information with generative AI to produce concise, accurate, and context-aware updates.
   - Covers diverse topics, including academic announcements, safety alerts, and cultural events.

5. *Interactive Frontend*:
   - Developed using *Streamlit* to allow students to input queries, view updates, and upload custom documents for analysis.

6. *Automation with Pipelines*:
   - Integrates *Apache Airflow* to manage real-time data ingestion pipelines, ensuring updates are current and efficient.

---

## *Benefits of RAG in this Project*
- *Context-Aware Retrieval*: Combines semantic search with generative capabilities for precise and meaningful updates.
- *Real-Time Insights*: Automates data ingestion and processing to deliver updates as events occur.
- *Scalability*: Supports growing data and user demands while maintaining performance.

---

## *Tools and Technologies Used*

### *Data Collection and Preprocessing*:
- *Google Cloud Document AI*: Parsing structured information from documents.
- *BeautifulSoup*: Web scraping data from university websites and news sources.
- *Python*: Primary language for preprocessing and integration.

### *Semantic Search and Retrieval*:
- *Milvus, **Pinecone, **Qdrant, **Weaviate*: Vector databases for storing and retrieving semantic embeddings.

### *Natural Language Processing and Generation*:
- *OpenAI GPT-3.5/4*: For query understanding, data generation, and news summarization.

### *Automation and Workflow Management*:
- *Apache Airflow*: For real-time data ingestion and process automation.

### *Frontend Development*:
- *Streamlit*: For creating an interactive user interface.

### *Deployment and Scalability*:
- *Docker*: For containerization and ensuring scalability.

### *Data Analytics and Insights*:
- *AutoML*: For predictive analytics and enhancing system recommendations.

### *Additional Tools*:
- *Git/GitHub*: For version control and collaboration.
- *Pandas and NumPy*: For data manipulation and statistical analysis.

---

## *Future Scope*
The *AI University News Generator* has significant potential for future enhancements:

1. *Expansion to Multiple Campuses*:
   - Adapt to diverse data sources for centralized inter-campus news aggregation.

2. *Mobile Application Development*:
   - Develop a mobile-friendly version with push notifications.

3. *Advanced Personalization*:
   - Implement advanced machine learning models for hyper-personalized news feeds.

4. *Integration with Existing University Systems*:
   - Seamlessly integrate with LMS platforms, bulletin boards, and student portals.

5. *Multi-Language Support*:
   - Add multilingual capabilities for global accessibility.

6. *Sentiment Analysis and Prioritization*:
   - Use sentiment analysis to prioritize critical updates.

7. *Community Engagement Features*:
   - Introduce forums for student interactions and peer-to-peer collaboration.

8. *AI-Driven Alerts and Predictions*:
   - Use predictive analytics to notify students about deadlines or disruptions.

---

## *Challenges Faced*
- *Data Collection and Quality*: Managing diverse and unstructured data.
- *Scalability*: Ensuring performance for large datasets and queries.
- *Semantic Search Accuracy*: Maintaining relevance for diverse queries.
- *Integration Challenges*: Collaborating with university systems.
- *Security and Privacy*: Protecting sensitive student information.
- *Deployment and Maintenance*: Managing resource-intensive AI models.
- *User Adoption*: Encouraging regular platform use through usability and features.

---

## *Reference*
This project references and utilizes tools, frameworks, and methodologies from the following sources:
1. *Google Cloud Document AI*: Document parsing and structured information extraction.
2. *BeautifulSoup*: Web scraping for university websites.
3. *OpenAI GPT Models*: Query understanding and generative responses.
4. *Pinecone, Milvus, Qdrant, Weaviate*: Vector storage and retrieval.
5. *Apache Airflow*: Real-time pipeline management.
6. *Streamlit*: Interactive user interface development.
7. *Docker*: Containerization for deployment.
8. *LangChain*: Task chaining for LLM workflows.
9. *AutoML*: Predictive analytics for recommendations.
10. *Pandas and NumPy*: Data preprocessing and manipulation.

---

## *License*
This project is licensed under the *MIT License*.

### *Permissions*:
- Commercial use
- Distribution
- Modification
- Private use

### *Conditions*:
- Attribution must be provided in the project documentation and any redistributed code.

### *Limitations*:
- The software is provided "as is," without warranty of any kind.

Full license text: [MIT License Details](https://opensource.org/licenses/MIT).

---

## *Conclusion*
The *AI University News Generator* redefines how students stay informed, offering precise, personalized, and timely updates by integrating *GPT LLMs, **vector databases, and **document parsing tools*. This platform fosters a more connected and engaged university community while laying the foundation for future scalability and innovation.
