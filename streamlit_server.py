import streamlit as st
import requests
import json

folder_id = 'b1gql3ul5bq1rbuv2fvg'
IAM_token = "t1.9euelZqRnM6enpOZx8zOlJuPj5KLje3rnpWanoyZxo7HxpOKio-Yx8qVjpDl8_coDxdP-e8ADEEZ_t3z92g9FE_57wAMQRn-zef1656Vmo2Xm5aQlc6Xz5eWzcuYyZ6W7_zF656Vmo2Xm5aQlc6Xz5eWzcuYyZ6W.TqptZAHdY7S0fmBlPf0b0EB5MUnHGpaIqgnzNGjxHulyfEbQTExCtfrJa9_0bJuGldv7vKOjm7WD8O9WFOeiCw"


# temporary token


def request_YandexGPT(text_list, folder_id, IAM_token):
    prompt = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",

        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Я готовлю датасет для перевода предложений из неформального языка в формальный. У меня есть набор русских твитов, можешь сделать текст более официальным и формальным. Напиши этот текст будто ты профессор русского языка. Проверь, что в ответе нет матов, и разговорных слов. Избегай неофициальных слов. Заменяй маты во всех их вариациях! Старайся сохранить эмоцию автора. Убедись, что выходные данные пронумерованы с нуля. На каждый вход ровно один выход. Для разделения используй символ '\n'. Выведи только исправленный список, не выводи лишнего."
            },
            {
                "role": "user",
                "text": str(text_list)
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IAM_token}",
        "x-folder-id": folder_id

    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    return json.loads(result)['result']['alternatives'][0]['message']['text']


API_URL = "https://api-inference.huggingface.co/models/VorArt/Formalist"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response = response.json()
    if len(response) == 0:
        response = [{"generated_text": "Прошу прощения, но я не смог это обработать"}]
    return response


if "last" not in st.session_state:
    st.session_state.last = ''

st.title("Informal to formal")

text = st.text_area("Введите текст в неформальной форме", max_chars=300, height=150)

if st.button("Перевести"):
    st.session_state.last = query({
        "inputs": text,
        "parameters": {
            "max_length": 300,
            "num_return_sequences": 1,
            "temperature": 0.5,
            "do_sample": True,
            "top_k": 50,
            "top_p": 0.92,
            "repetition_penalty": 1.2
        }
    })[0]["generated_text"]
st.text_area("Ответ", max_chars=300, height=150, value=st.session_state.last)
st.text("Помогите дообучить модель, как вам перевод конкретно этого предложения?")

c1, c2, c3, c4, c5, c6 = st.columns(6)
if c1.button("Хорошо"):
    st.text("Спасибо за оценку!!!")

if c2.button("Плохо"):
    st.text("Спасибо за оценку!!!")

if st.button("Хочу увидеть что ответит Yandex-GPT"):
    if text.strip() != '':
        value = request_YandexGPT(text, folder_id, IAM_token)

        st.text_area("вот что выдал Yandex-GPT:", max_chars=300, height=150, value=value)
    else:
        st.text("Напишите хоть что-то...")
