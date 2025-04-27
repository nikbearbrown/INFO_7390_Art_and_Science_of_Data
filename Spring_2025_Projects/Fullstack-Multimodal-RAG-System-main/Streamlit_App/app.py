import os
import requests
import streamlit as st
from datetime import datetime, timezone

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ─────────────────────────  PAGE CONFIG & GLOBAL CSS  ─────────────────────────
st.set_page_config(page_title="Multimodal RAG", page_icon="📄", layout="wide")

st.markdown(
    """
    <style>
      body            {background:#f7f9fc; font-family:"Trebuchet MS",sans-serif;}
      .block-container{padding-top:2.5rem;}
      h1,h2,h3,h4     {color:#003366;}
      .stButton>button{background:#003366;border:none;color:white;
                       padding:0.5rem 1.1rem;border-radius:4px;font-size:0.9rem;}
      .stButton>button:hover{background:#00509e;}
      .chat-bubble    {padding:0.6rem 0.9rem;border-radius:12px;margin-bottom:0.5rem;
                       max-width:80%;word-wrap:break-word;}
      .user-bubble    {background:#00509e;color:white;margin-left:auto;}
      .ai-bubble      {background:#e1ecf7;color:#000;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────  SESSION DEFAULTS  ────────────────────────────────
_defaults = {
    "logged_in": False,
    "token": None,
    "username": None,
    "page": "home",          # home | signin | signup | chat
    "indexes": [],
    "selected_index": None,
    "chat_history": [],
}
for k, v in _defaults.items():
    st.session_state.setdefault(k, v)

# ─────────────────────────  HELPERS  ─────────────────────────────────────────
def _rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.rerun()

def _reset_session():
    st.session_state.update({
        "logged_in": False,
        "token": None,
        "username": None,
        "indexes": [],
        "selected_index": None,
        "chat_history": [],
    })

def _auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}

def _handle_401(resp: requests.Response):
    if resp.status_code == 401:
        st.warning("Session expired – please log in again.")
        _reset_session(); st.session_state.page = "signin"; _rerun()

# ─────────────────────────  PUBLIC HOME  ─────────────────────────────────────
def public_home():
    st.markdown('<h1 style="text-align:center;">Multimodal Retrieval-Augmented Generation System</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;">Your AI-powered Multimodal RAG Assistant</h3>', unsafe_allow_html=True)
    st.write("---")
    st.markdown(
        """
        <div style="text-align:center;font-size:1.1rem;">
          📚 <b>Document Selection</b>  |  💡 <b>Multimodal&nbsp;RAG</b>  |
          📝 <b>Interactive&nbsp;Q/A</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("---")
    st.markdown(
        """
        <div style="margin: 2rem auto; max-width: 800px; font-size:1.1rem; line-height:1.7;">
        <b>What is this?</b><br>
        The Multimodal Retrieval-Augmented Generation System is an advanced AI application designed to help you search, analyze, and interact with complex documents-especially CFA publications and financial PDFs-using the latest in multimodal AI technology.
        <br><br>
        <b>How does it work?</b>
        <ul>
          <li><b>Data Scraping & Ingestion:</b> Automatically collects CFA publications, loading PDFs to Google Cloud Platform (GCP).</li>
          <li><b>PDF Parsing:</b> Extracts both text and images using <b>pymupdf4llm</b> and <b>Upstage Document API</b> for rich, multimodal understanding.</li>
          <li><b>Vectorization:</b> Converts extracted text into high-performance search indexes using <b>OpenAI embeddings</b> and <b>Pinecone</b> vector store.</li>
          <li><b>Multimodal Q/A:</b> Enables you to ask questions about both text and images, powered by <b>OpenAI GPT-4o</b> and <b>Gemini 2.5 Pro</b> for robust, context-aware answers.</li>
          <li><b>Modern Deployment:</b> Runs securely in Docker containers, orchestrated via Docker Compose and deployed on GCP for scalability and reliability.</li>
        </ul>
        <b>Tech Stack Highlights:</b>
        <ul>
          <li>PDF Parsing: <b>pymupdf4llm</b>, <b>Upstage Document API</b></li>
          <li>AI & Multimodal Data: <b>Gemini 2.5 Pro</b>, <b>OpenAI GPT-4o</b></li>
          <li>Vector Store: <b>Pinecone</b></li>
          <li>Frontend: <b>Streamlit</b> | Backend: <b>FastAPI</b></li>
        </ul>
        <b>What can you do?</b>
        <ul>
          <li>Chat with your financial documents: Ask questions about tables, charts, or text.</li>
          <li>Search across multiple documents with lightning-fast, AI-powered retrieval.</li>
          <li>Get context-rich, multimodal answers-instantly.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("---")
    st.markdown('<div style="text-align:center;font-size:1.5rem;">🚀 Click <b>🔒 Login</b> to get started</div>', unsafe_allow_html=True)

# ─────────────────────────  CHAT UTILITIES  ─────────────────────────────────-
def _load_indexes():
    resp = requests.get(f"{API_URL}/indexes", headers=_auth_headers())
    _handle_401(resp)
    if resp.ok:
        st.session_state.indexes = resp.json().get("indexes", [])
        if st.session_state.indexes and st.session_state.selected_index not in st.session_state.indexes:
            st.session_state.selected_index = st.session_state.indexes[0]
    else:
        st.error(resp.json().get("detail", resp.text))

def chat_page():
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Hi, {st.session_state.username}")
        st.caption("You are logged in. Use the controls below to manage your session and indexes.")

        if st.button("🚪 Logout"):
            _reset_session(); st.session_state.page = "home"; _rerun()

        st.write("---")
        st.markdown("#### 📄 Manage Document Indexes")
        st.caption("Indexes represent collections of parsed documents you can chat with.")

        if st.button("🔄 Refresh Indexes") or not st.session_state.indexes:
            _load_indexes()

        if st.session_state.indexes:
            st.session_state.selected_index = st.selectbox(
                "📂 Select an Index",
                st.session_state.indexes,
                index=st.session_state.indexes.index(st.session_state.selected_index)
                if st.session_state.selected_index in st.session_state.indexes else 0,
                help="Choose which document collection to chat with."
            )
            st.success(f"Active index: {st.session_state.selected_index}")
        else:
            st.info("No indexes available. Please upload or refresh.")

        st.write("---")
        st.markdown("#### 💡 Tips")
        st.markdown(
            """
            - Ask about tables, figures, or any content in your documents.
            - Use clear, specific questions for best results.
            - Switch indexes to chat with different document sets.
            """
        )

    # Main area
    st.markdown("<h2>💬 Chat with Your Documents</h2>", unsafe_allow_html=True)
    st.caption("Type your question below to interact with your selected document index. The assistant can answer questions about both text and images in your PDFs.")

    # Show chat history with clear roles and timestamps (if available)
    for msg in st.session_state.chat_history:
        cls = "user-bubble" if msg["role"] == "user" else "ai-bubble"
        role = "You" if msg["role"] == "user" else "Assistant"
        timestamp = (
            f"<span style='font-size:0.8em;color:#888;'>[{msg.get('timestamp','')[:19].replace('T',' ')}]</span>"
            if "timestamp" in msg else ""
        )
        st.markdown(
            f'<div class="chat-bubble {cls}"><b>{role}:</b> {msg["content"]} {timestamp}</div>',
            unsafe_allow_html=True
        )

    # Chat input
    query = st.chat_input("Ask something…")
    if query and st.session_state.selected_index:
        now = datetime.now(timezone.utc).isoformat()
        st.session_state.chat_history.append({"role": "user", "content": query, "timestamp": now})
        st.markdown(f'<div class="chat-bubble user-bubble"><b>You:</b> {query}</div>', unsafe_allow_html=True)

        # Show spinner while waiting for backend
        with st.spinner("Generating answer…"):
            payload = {"question": query, "top_k": 10}
            resp = requests.post(
                f"{API_URL}/qa/{st.session_state.selected_index}",
                json=payload,
                headers=_auth_headers(),
            )
            _handle_401(resp)
            answer = resp.json().get("answer", "<no answer>") if resp.ok else f"Error: {resp.text}"

        now = datetime.now(timezone.utc).isoformat()
        st.session_state.chat_history.append({"role": "assistant", "content": answer, "timestamp": now})
        st.markdown(f'<div class="chat-bubble ai-bubble"><b>Assistant:</b> {answer}</div>', unsafe_allow_html=True)

    # Optional: Add a divider and a short help section at the bottom
    st.write("---")
    st.markdown(
        """
        <div style="font-size:0.95em;color:#555;">
            <b>About:</b> This chat uses advanced Retrieval-Augmented Generation (RAG) to answer your queries using both text and images from your selected documents.<br>
            <b>Powered by:</b> OpenAI, Gemini, Pinecone, Document AI.
        </div>
        """,
        unsafe_allow_html=True
    )


# ─────────────────────────  SIGN IN / SIGN UP  ───────────────────────────────
def signin_page():
    st.markdown("<h2>🔐 Sign In</h2>", unsafe_allow_html=True)
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("➡️ Sign In"):
        if not username or not password:
            st.warning("Enter both username and password."); return
        resp = requests.post(f"{API_URL}/login", data={"username": username, "password": password})
        if resp.ok:
            st.session_state.update({
                "token": resp.json()["access_token"],
                "logged_in": True,
                "username": username,
                "page": "chat",
                "chat_history": [],
                "indexes": [],
                "selected_index": None,
            }); _rerun()
        else:
            st.error(resp.json().get("detail", resp.text))

    st.write("Don't have an account?")
    if st.button("📝 Sign Up"):
        st.session_state.page = "signup"; _rerun()
    if st.button("🔙 Back"):
        st.session_state.page = "home"; _rerun()

def signup_page():
    st.markdown("<h2>🔑 Sign Up</h2>", unsafe_allow_html=True)
    email    = st.text_input("📧 Email")
    username = st.text_input("👤 Username")
    pwd1     = st.text_input("🔒 Password", type="password")
    pwd2     = st.text_input("🔒 Confirm Password", type="password")

    if st.button("✅ Register"):
        if not all([email, username, pwd1, pwd2]):
            st.warning("Fill in all fields."); return
        if pwd1 != pwd2:
            st.warning("Passwords do not match."); return
        resp = requests.post(f"{API_URL}/register", json={"email": email, "username": username, "password": pwd1})
        if resp.ok:
            st.success("Registered – please log in."); st.session_state.page = "signin"; _rerun()
        else:
            st.error(resp.json().get("detail", resp.text))

    if st.button("🔙 Back"):
        st.session_state.page = "signin"; _rerun()

# ─────────────────────────  ROUTER  ──────────────────────────────────────────
def main():
    if st.session_state.page == "home":
        col1, col2 = st.columns([8,1])
        with col2:
            if st.session_state.logged_in:
                if st.button("🚪 Logout"): _reset_session(); _rerun()
            else:
                if st.button("🔒 Login"): st.session_state.page = "signin"; _rerun()
        public_home()

    elif st.session_state.page == "signin":
        signin_page()

    elif st.session_state.page == "signup":
        signup_page()

    elif st.session_state.page == "chat":
        if not st.session_state.logged_in:
            st.session_state.page = "signin"; _rerun()
        chat_page()

    else:
        st.error("Unknown page")

if __name__ == "__main__":
    main()