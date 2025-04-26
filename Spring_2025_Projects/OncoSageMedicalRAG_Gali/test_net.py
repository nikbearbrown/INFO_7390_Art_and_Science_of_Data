import socket

host = "medical-knowledge-m4vk4fg.svc.aped-4627-b74a.pinecone.io"
port = 443
try:
    with socket.create_connection((host, port), timeout=5):
        print(f"✅ {host}:{port} is reachable")
except Exception as e:
    print(f"❌ Can’t connect to {host}:{port}: {e}")
