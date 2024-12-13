import pinecone

# Initialize Pinecone with just the API key
pinecone.init(api_key='xxx')

# Print the list of environments
print("Available Pinecone Environments:")
for env in pinecone.list_indexes():
    print(env)
