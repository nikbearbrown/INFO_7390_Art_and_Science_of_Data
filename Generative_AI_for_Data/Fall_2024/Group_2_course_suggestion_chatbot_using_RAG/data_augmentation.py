from pinecone import Pinecone
import pandas as pd
from connections import pinecone_connection, openai_connection
from openai import OpenAI

def storing_pinecone():
    '''
    function to store set a in pinecone
    '''
    df = pd.read_csv("output/ExtractedCourseDescriptions.csv")
    print(df.head())

    # Group by CourseID and apply transformation
    grouped = df.groupby('CourseID', group_keys=False).apply(lambda group: {
        "Course Name": group['Course Name'].iloc[0],  # Unique per CourseID
        # Unique per CourseID
        "Course Description": group['Course Description'].iloc[0],
        "CRNs": group['CRN'].tolist(),  # All CRNs for this CourseID
        # All Instructors for this CourseID
        "Instructors": group['Instructor'].tolist(),
        # All Timings for this CourseID
        "Timings": group['Timings'].tolist()
    }).reset_index(name='Grouped Data')

    print(grouped.head())  # Display the first few rows of grouped data

    # openai
    api_key = openai_connection()
    openai_client = OpenAI(api_key=api_key)

    # Pinecone
    pinecone_api_key, index_name = pinecone_connection()
    pinecone = Pinecone(api_key=pinecone_api_key)
    index = pinecone.Index(name=index_name)

    try:

        all_embeddings = []

        print("Generating embeddings...")
        # Generate embeddings for each group
        for _, row in grouped.iterrows():
            course_id = row['CourseID']
            data = row['Grouped Data']

            details = (
    f"{course_id} {data['Course Name']} {data['Course Description']} "
    f"CRNs: {', '.join(map(str, data['CRNs']))} "
    f"Instructors: {', '.join(data['Instructors'])} "
    f"Timings: {', '.join(data['Timings'])}"
)



            # Embedding data
            embedding = openai_client.embeddings.create(
                input=details,
                model='text-embedding-ada-002'
            ).data[0].embedding

            print(f"Embedded data for CourseID: {course_id}")

            embedding_data = {
                "id": course_id,
                "values": embedding,
                "metadata": {
                    "Course ID": course_id,
                    "Course Name": data['Course Name'],
                    "CRNs": [str(crn) for crn in data['CRNs']],
                    "Instructors": data['Instructors'],
                    "Timings": data['Timings'],
                    "Course Description": data['Course Description']
                }
            }


            all_embeddings.append(embedding_data)

        print("Embeddings generated")

        # upserting the embeddings to pinecone namespace
        index.upsert(all_embeddings)

        return "successful"

    except Exception as e:
        print("Exception in storing_pinecone() function: ", e)
        return "failed"
    
'''
if __name__ == "__main__":
    storing_pinecone()
'''