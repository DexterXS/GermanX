import streamlit as st
import random


class Card:
    def __init__(self, term, translation, category):
        self.term = term
        self.translation = translation
        self.category = category


class FlashcardApp:
    def __init__(self):
        if 'flashcards' not in st.session_state:
            st.session_state.flashcards = []

    def add_flashcard(self):
        term = st.text_input("Термін:")
        translation = st.text_input("Переклад:")
        category = st.text_input("Категорія:")

        if term and translation and category:
            st.session_state.flashcards.append(Card(term, translation, category))
            st.success("Картку додано!")

    def study_flashcards(self):
        if not st.session_state.flashcards:
            st.warning("Додайте картку перед вивченням.")
            return

        random_card = random.choice(st.session_state.flashcards)
        user_translation = st.text_input(f"Як перекладеться '{random_card.term}'?")

        if user_translation:
            if user_translation.lower() == random_card.translation.lower():
                st.success("Вірно!")
            else:
                st.error(f"Правильний переклад: {random_card.translation}")

    def view_all_flashcards(self):
        if not st.session_state.flashcards:
            st.warning("Додайте картку перед переглядом.")
            return

        st.header("Всі картки")
        for card in st.session_state.flashcards:
            st.button(f"{card.term}\nПереклад: {card.translation}\nКатегорія: {card.category}")

    def choose_category(self):
        categories = list(set(card.category for card in st.session_state.flashcards))
        selected_category = st.selectbox("Виберіть категорію:", ["Всі"] + categories)

        selected_flashcards = st.session_state.flashcards if selected_category == "Всі" else [
            card for card in st.session_state.flashcards if card.category == selected_category
        ]

        st.header(f"Картки в категорії: {selected_category}")
        for card in selected_flashcards:
            st.button(f"{card.term}\nПереклад: {card.translation}")


def main():
    st.title("Додаток з мовними картками")

    app = FlashcardApp()

    menu = ["Додати картку", "Вивчати картки", "Переглянути всі картки", "Вибрати картки за категорією"]
    choice = st.sidebar.selectbox("Виберіть опцію", menu)

    if choice == "Додати картку":
        app.add_flashcard()
    elif choice == "Вивчати картки":
        app.study_flashcards()
    elif choice == "Переглянути всі картки":
        app.view_all_flashcards()
    elif choice == "Вибрати картки за категорією":
        app.choose_category()


if __name__ == "__main__":
    main()