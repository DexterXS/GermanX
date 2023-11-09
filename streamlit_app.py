import streamlit as st
from gpt4all import GPT4All
model = GPT4All("mistral-7b-openorca.Q4_0.gguf")


# Установка заголовка страницы
st.title("Пример веб-приложения с Streamlit")

# Добавление кнопки
if st.button("Нажми меня"):
    st.write("Кнопка была нажата!")

    # Добавление поля для ввода текста
user_input = st.text_input("Введите текст", max_chars=80)

with model.chat_session():
    response1 = model.generate(prompt=user_input, temp=0)
    st.write("Відповідь:", model.current_chat_session)