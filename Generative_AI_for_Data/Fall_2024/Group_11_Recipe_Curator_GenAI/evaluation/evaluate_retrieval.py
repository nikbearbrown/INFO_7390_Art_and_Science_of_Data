import json
import requests

# Load test data
def load_test_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Precision@K metric
def precision_at_k(retrieved_ids, relevant_ids, k):
    retrieved_k = set(retrieved_ids[:k])
    relevant_set = set(relevant_ids)
    return len(retrieved_k & relevant_set) / k

# Recall metric
def recall(retrieved_ids, relevant_ids):
    relevant_set = set(relevant_ids)
    return len(set(retrieved_ids) & relevant_set) / len(relevant_set)

# Mean Reciprocal Rank (MRR) metric
def mean_reciprocal_rank(retrieved_ids, relevant_ids):
    for rank, item in enumerate(retrieved_ids, 1):
        if item in relevant_ids:
            return 1 / rank
    return 0

# Evaluate retrieval
def evaluate_retrieval(test_data, api_endpoint):
    results = []

    for test in test_data:
        query = test["query"]
        relevant_ids = test["relevant_ids"]

        # Call the retrieval API
        response = requests.post(f"{api_endpoint}/search_recipes/", json={"query": query, "session_id": "test-session"})
        if response.status_code == 200:
            retrieved_ids = [float(recipe["RecipeId"]) for recipe in response.json()["recipes"]]

            # Debugging logs
            print(f"Query: {query}")
            print(f"Relevant IDs: {relevant_ids}")
            print(f"Retrieved IDs: {retrieved_ids}")

            # Calculate metrics
            precision = precision_at_k(retrieved_ids, relevant_ids, k=5)
            recall_score = recall(retrieved_ids, relevant_ids)
            mrr_score = mean_reciprocal_rank(retrieved_ids, relevant_ids)

            results.append({
                "query": query,
                "precision@5": precision,
                "recall": recall_score,
                "mrr": mrr_score
            })
        else:
            results.append({"query": query, "error": "API call failed"})

    return results

# Main function
if __name__ == "__main__":
    # Load test data
    test_data = load_test_data("test_data.json")

    # Define API endpoint
    api_endpoint = "http://0.0.0.0:8000"

    # Evaluate retrieval
    results = evaluate_retrieval(test_data, api_endpoint)

    # Print results
    for result in results:
        print(result)
        
