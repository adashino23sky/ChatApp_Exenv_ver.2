import streamlit as st
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


messages = [
    SystemMessage("you're a good assistant, you always respond with a joke."),
    HumanMessage(content = human_input),
    AIMessage(
        content = ai_output
    ),
    HumanMessage("and who is harrison chasing anyways"),
    AIMessage(
        "Hmmm let me think.\n\nWhy, he's probably chasing after the last cup of coffee in the office!"
    ),
    HumanMessage("what do you call a speechless parrot"),
]


import firebase_admin
from firebase_admin import credentials

# Show title and description.
st.title("")

openai_api_key = st.secret("openAIAPI.key")
if not openai_api_key:
    st.info("Please add your OpenAI API key to secret to continue.", icon="🗝️")
else:
    # APIクライアント作成
    client = OpenAI(api_key=openai_api_key)
    
    llm = ChatOpenAI(model="gpt-4o-mini")

    # システムプロンプト作成
    with open('prompt.txt', encoding = 'UTF-8', mode = 'r') as f:
        system_template = f.read()

    # # 会話のテンプレートを作成
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}"),
])
    # 会話格納コンテナ初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 会話履歴可視化
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 会話入力
    if input_message := st.chat_input("あなたの意見を入力してください"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(input_message)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # firebase認証
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
