import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

load_dotenv('./.env')

st.set_page_config(page_title="My Chatbot")
st.title("My Local Chatbot")
st.write("Chat with me! Built with Streamlit, LangChain & Ollama.")

BASE_URL = "http://localhost:11434"
MODEL_NAME = 'llama3.2:3b'

user_id = st.text_input("Enter your user ID:", "user1")

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Start New Conversation"):
    st.session_state.chat_history = []
    history = get_session_history(user_id)
    history.clear()

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

llm = ChatOllama(base_url=BASE_URL, model=MODEL_NAME)

system_prompt = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")
human_prompt = HumanMessagePromptTemplate.from_template("{input}")
messages = [system_prompt, MessagesPlaceholder(variable_name='history'), human_prompt]

prompt_template = ChatPromptTemplate(messages=messages)
chain = prompt_template | llm | StrOutputParser()

runnable_with_history = RunnableWithMessageHistory(
    chain, 
    get_session_history, 
    input_messages_key='input', 
    history_messages_key='history'
)

def chat_with_llm(session_id, user_input):
    for token in runnable_with_history.stream(
        {'input': user_input}, 
        config={'configurable': {'session_id': session_id}}
    ):
        yield token

user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.chat_history.append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = st.write_stream(chat_with_llm(user_id, user_input))
    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
