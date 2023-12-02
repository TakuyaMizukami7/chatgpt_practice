
import streamlit as st
from openai._client import OpenAI

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
client = OpenAI(api_key = st.secrets.OpenAIAPI.openai_api_key,)

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
      {"role": "system",
       "content": "あなたは優秀なAIアシスタントです"
       }
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = client.chat.completions.create(
      messages = messages,
      model = "gpt-3.5-turbo",
      # 乱雑さ「temperature」を設定
      temperature =  0.8
    )

    bot_message = response.choices[0].message
    #OpenAIからの回答がJSON配列で返ってくるため、必要な情報を抜き出し辞書型で格納
    bot_message_dict = {"role": bot_message.role, "content": bot_message.content}

    messages.append(bot_message_dict)

    st.session_state["user_input"] = "" #入力欄の消去

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]): #直近のメッセージを上に
        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "🤖"
            st.write(speaker + ": " + message["content"])
