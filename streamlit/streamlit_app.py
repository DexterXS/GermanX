import streamlit as st
import numpy as np

# Создаем случайные данные
np.random.seed(42)
data = np.random.randn(100, 2)

# Заголовок приложения
st.title('Пример Streamlit без сторонних библиотек')

# Выводим таблицу данных
st.write('Случайные данные:', data)

# Выводим график с использованием встроенных средств Streamlit
st.line_chart(data)

# Добавляем интерактивные элементы управления
selected_rows = st.multiselect('Выберите строки', list(range(100)))
if selected_rows:
    st.write('Выбранные строки:')
    st.write(data[selected_rows])
