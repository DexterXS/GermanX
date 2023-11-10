import streamlit as st
import spacy
from annotated_text import annotated_text

# Загрузка модели spaCy для немецкого языка
nlp = spacy.load("de_core_web_sm")


# Функция для выделения глаголов в тексте
def highlight_verbs(text):
    doc = nlp(text)
    highlighted_text = []
    for token in doc:
        if token.pos_ == "VERB" or (token.dep_ == "aux" and token.head.pos_ == "VERB"):
            highlighted_text.append((token.text, "verb"))
        else:
            highlighted_text.append(token.text)
    return highlighted_text


# Веб-приложение с использованием Streamlit
def main():
    st.title("Text Highlighter")

    # Поле для ввода текста пользователем
    user_text = st.text_area("Введите текст:")

    if st.button("Выделить глаголы"):
        # Обработка текста и выделение глаголов
        highlighted_text = highlight_verbs(user_text)

        # Отображение выделенного текста
        annotated_text(*highlighted_text)


if __name__ == "__main__":
    main()
