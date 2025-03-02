import requests
import streamlit as st

import config as config
from helper import display_duration

st.set_page_config(
    page_title="Chat with the ESPN RSS Feed",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("Chat with the ESPN RSS Feed")

col1, col2 = st.columns([9, 2])
with col2:
    if st.button("Reset"):
        response = requests.post(f"{config.BACKEND_HOST}/reset")
        if response.ok:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": config.TITLE,
                }
            ]


if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": config.TITLE,        
        }
    ]


if prompt := st.chat_input(
    "Ask a question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages:  # Write message history to UI
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant":
            duration = message.get("duration", None)
            if duration:
                st.markdown(display_duration(duration), unsafe_allow_html=True)
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.get(f"{config.BACKEND_HOST}/query?query={prompt}")
            if response.ok:
                response_data = response.json()
                output = response_data["answer"]
                output = (
                    output
                    + "\n\n"
                    + "reference links: \n"
                    + ", ".join(response_data["document_links"])
                )
                st.write(output)
                duration = round(response.elapsed.total_seconds(), 2)
                st.markdown(display_duration(duration), unsafe_allow_html=True)
                message = {"role": "assistant",
                           "content": output, "duration": duration}
                # Add response to message history
                st.session_state.messages.append(message)
            else:
                st.write("apologies, we are experiencing errors")
