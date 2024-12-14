import subprocess
import tempfile
import threading
import os
 
def create_codelab_from_string(content):
    metadata = (
        "id: chatbot-generated-codelab\n"
        "title: Chatbot Generated Codelab\n"
        "summary: This is a response codelab generated from chatbot content.\n"
        "category: Chatbot\n"
        "tags: chat,bot,AI\n"
        "status: Draft\n"
        "authors: dipen@example.com\n\n"
    )
    content_with_metadata = metadata + content
 
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_file.write(content_with_metadata)
        temp_file_path = temp_file.name
    try:
        result = subprocess.run(['claat', 'export', temp_file_path],
                                capture_output=True, text=True, check=True)
        print("Codelab created successfully!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("Error creating codelab:", e.stderr)
    finally:
        os.unlink(temp_file_path)

# def serve_codelab():
#     codelab_id = 'chatbot-generated-codelab'
#     os.chdir(codelab_id)
#     subprocess.run(['claat', 'serve', '-addr', '0.0.0.0:9090'])

# Function to serve the codelab
def serve_codelab():
    codelab_id = 'chatbot-generated-codelab'
    subprocess.run(['claat', 'serve', '-addr', '0.0.0.0:9090'], cwd=codelab_id)

# Start the codelab server in a background thread
def start_codelab_server():
    server_thread = threading.Thread(target=serve_codelab, daemon=True)
    server_thread.start()