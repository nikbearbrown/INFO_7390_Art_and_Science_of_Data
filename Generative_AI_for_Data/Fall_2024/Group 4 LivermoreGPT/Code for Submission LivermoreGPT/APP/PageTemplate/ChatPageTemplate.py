import streamlit as st


def ChatPageTemplate(subHeader = None, description = None, chatFunction = None, streamSupported = False):

    st.title("LivermoreGPT")
    if subHeader:
        st.subheader(subHeader)
    if description:
        st.write(description)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = chatFunction();

            if streamSupported:
                response = st.write_stream(stream)
            else:
                response = st.write(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
