import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("")

openai_api_key = st.secret("openAIAPI.key")
if not openai_api_key:
    st.info("Please add your OpenAI API key to secret to continue.", icon="🗝️")
else:
    # client作成
    client = OpenAI(api_key=openai_api_key)
    # 会話格納コンテナ初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 会話履歴可視化
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 会話入力
    if prompt := st.chat_input("あなたの意見を入力してください"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

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
