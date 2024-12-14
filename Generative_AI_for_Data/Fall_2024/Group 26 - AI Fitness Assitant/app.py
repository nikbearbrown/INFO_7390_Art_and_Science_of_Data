import streamlit as st
from create_vector_database import query_index
from llm_integrations import get_response_from_llm

# Streamlit App Configuration
st.set_page_config(
    page_title="AI-Powered Fitness Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for chat history and temporary input storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "temp_input" not in st.session_state:
    st.session_state.temp_input = ""

# Title and Description
st.title("💬 AI-Powered Fitness Chat")
st.markdown(
    """
    Welcome to your personalized fitness assistant!  
    Engage in a conversational experience by asking any fitness-related questions.
    """
)

# Chat Display Section
st.header("Chat")
chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['text']}")
        elif chat["role"] == "assistant":
            st.markdown(f"**AI:** {chat['text']}")
        elif chat["role"] == "context":
            st.markdown(f"**Context Retrieved:**\n{chat['text']}")

# Divider
st.divider()

# Input Section
query_text = st.text_input(
    "Type your message:",
    value=st.session_state.temp_input,
    placeholder="Ask me anything about fitness...",
)

# Handle User Query
if st.button("Send"):
    if query_text.strip():
        # Add user query to chat history
        st.session_state.chat_history.append({"role": "user", "text": query_text})

        # Retrieve relevant context
        with st.spinner("Fetching relevant contexts..."):
            context_results = query_index(query_text)

        if context_results:
            # Add retrieved context to chat history
            
            st.session_state.chat_history.append({"role": "context", "text": context_results})

        # Prepare context from previous chat history
        previous_responses = "\n".join(
            [f"AI: {item['text']}" for item in st.session_state.chat_history if item["role"] == "assistant"]
        )
        prompt = f"Using previous responses and the user's new query:\n\nPrevious Responses:\n{previous_responses}\n\nNew Query: {query_text}"

        # Generate response from LLM
        with st.spinner("AI is typing..."):
            response = get_response_from_llm(prompt)

        # Add LLM response to chat history
        st.session_state.chat_history.append({"role": "assistant", "text": response})

        # Clear the input box
        st.session_state.temp_input = ""

        # Rerun to update chat
        st.rerun()
    else:
        st.error("Please enter a valid question.")

# Footer Section
st.markdown(
    """
    ---
    **Powered by:**  
    - **[Pinecone](https://www.pinecone.io/?utm_term=pinecone%20vector%20database&utm_campaign=brand-us-e&utm_source=adwords&utm_medium=ppc&hsa_acc=3111363649&hsa_cam=21023369441&hsa_grp=167470667468&hsa_ad=690982708943&hsa_src=g&hsa_tgt=kwd-1538083228315&hsa_kw=pinecone%20vector%20database&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=Cj0KCQiA0--6BhCBARIsADYqyL_Bpdl1Ij39V2lhjdBWKBcUjBfqQVlSLWSalj6_EnkMdNaVLkkNPgUaAnJaEALw_wcB)** for vector database management.  
    - **[Google Generative AI](https://cloud.google.com/vertex-ai/docs/generative-ai/overview)** for advanced AI capabilities.  
    - **[Streamlit](https://streamlit.io/)** for an interactive frontend.
    """
)
