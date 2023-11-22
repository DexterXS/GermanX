import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Создаем случайные данные для графика
np.random.seed(42)
data = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'size': np.random.rand(100) * 10,
    'color': np.random.rand(100)
})

# Заголовок приложения
st.title('Пример Streamlit с Plotly')

# Выводим график с использованием Plotly Express
fig = px.scatter(data, x='x', y='y', size='size', color='color', opacity=0.7, title='Пример графика')
st.plotly_chart(fig)

# Добавляем интерактивные элементы управления
selected_points = st.multiselect('Выберите точки', data.index)
if selected_points:
    st.write('Выбранные точки:')
    st.write(data.loc[selected_points])