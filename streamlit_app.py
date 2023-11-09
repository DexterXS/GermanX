import streamlit as st

def main():
    # Установка заголовка страницы
    st.title("Пример веб-приложения с Streamlit")

    # Добавление кнопки
    if st.button("Нажми меня"):
        st.write("Кнопка была нажата!")

    # Добавление поля для ввода текста
    user_input = st.text_input("Введите текст", "По умолчанию")

    # Вывод текста, введенного пользователем
    st.write("Вы ввели:", user_input)

if __name__ == "__main__":
    main()