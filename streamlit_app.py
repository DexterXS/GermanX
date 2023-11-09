import streamlit as st
# Установка заголовка страницы
st.title("Пример веб-приложения с Streamlit")

# Добавление кнопки
if st.button("Нажми меня"):
    st.write("Кнопка была нажата!")

    # Добавление поля для ввода текста
user_input = st.text_input("Введите текст", max_chars=80)

    # Вывод текста, введенного пользователем
st.write("Вы ввели:", user_input)

