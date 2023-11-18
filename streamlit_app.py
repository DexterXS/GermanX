import streamlit as st
import spacy
from annotated_text import annotated_text
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базу данных SQLite
engine = create_engine("sqlite:///words.db", echo=True)
Base = declarative_base()


# Определяем модель для таблицы слов в базе данных
class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    word_type = Column(String, nullable=False)


# Создаем таблицу, если она не существует
Base.metadata.create_all(engine)


# Класс для работы с базой данных
class DatabaseManager:
    def __init__(self):
        self.engine = create_engine("sqlite:///words.db", echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_word(self, word, word_type):
        session = self.Session()
        new_word = Word(word=word, word_type=word_type)
        session.add(new_word)
        session.commit()
        session.close()


# Класс для обработки текста и выделения слов по ключам
class TextProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.db_manager = DatabaseManager()

    def highlight_words(self, text):
        doc = self.nlp(text)
        highlighted_text = []

        # Получаем ключи из базы данных
        keys = self.get_keys_from_database()

        for token in doc:
            if token.text.lower() in keys:
                highlighted_text.append((token.text, "key_word"))
            else:
                highlighted_text.append(token.text)

        return highlighted_text

    def get_keys_from_database(self):
        session = self.db_manager.Session()
        keys = [word.word.lower() for word in session.query(Word).all()]
        session.close()
        return keys


# Веб-приложение с использованием Streamlit
def main():
    st.title("Text Processor")

    # Создаем экземпляр класса TextProcessor
    text_processor = TextProcessor()

    # Поле для ввода текста пользователем
    user_text = st.text_area("Введите текст:")

    if st.button("Обработать текст"):
        # Обработка текста и выделение ключевых слов
        highlighted_text = text_processor.highlight_words(user_text)

        # Отображение выделенного текста
        annotated_text(*highlighted_text)


if __name__ == "__main__":
    main()