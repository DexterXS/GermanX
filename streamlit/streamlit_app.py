import streamlit as st
import requests
import pandas as pd
import plotly.express as px


def get_weather(api_key, city, units):
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        st.error(f"Помилка отримання погоди: {err}")
        return None


def get_weekly_forecast(api_key, city):
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=56")
        response.raise_for_status()
        return response.json()["list"]
    except requests.exceptions.RequestException as err:
        st.error(f"Помилка отримання тижневого прогнозу: {err}")
        return None


def display_weather(city, weather_data, units):
    main_data = weather_data.get("main", {})
    weather_info = weather_data.get("weather", [{}])[0]
    st.write(f"Погода у {city} зараз:", f"Температура: {main_data.get('temp')}°{units[0]}",
             f"Стан: {weather_info.get('description').capitalize()}", f"Вологість: {main_data.get('humidity')}%",
             f"Швидкість вітру: {weather_data.get('wind', {}).get('speed')} м/с")


def display_weekly_forecast(city, forecast_data):
    data = [{"Дата": item["dt_txt"], "Температура": f"{item['main']['temp']}°C",
             "Стан": item['weather'][0]['description'].capitalize()} for item in forecast_data]
    df = pd.DataFrame(data)
    st.write(f"Тижневий прогноз погоди для {city}:")
    st.table(df)


def display_weekly_temperature_chart(city, forecast_data):
    data = [{"Дата": item["dt_txt"], "Температура": item["main"]["temp"]} for item in forecast_data]
    df = pd.DataFrame(data)

    fig = px.line(df, x="Дата", y="Температура", title=f"Температурний режим у {city} на тиждень")
    fig.update_xaxes(type='category', categoryorder='array', categoryarray=['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'])
    st.plotly_chart(fig)


def main():
    st.title("Погодний та Графічний додаток")
    api_key = "ваш_фактичний_ключ_api"
    city = st.selectbox("Виберіть місто:", ["Kyiv", "New York", "Tokyo", "London"])
    units = st.radio("Одиниці вимірювання:", ["Цельсій", "Фаренгейт"])

    if st.button("Отримати погоду"):
        weather_data = get_weather(api_key, city, "metric" if units == "Цельсій" else "imperial")
        if weather_data:
            display_weather(city, weather_data, units)

    if st.button("Тижневий прогноз"):
        forecast_data = get_weekly_forecast(api_key, city)
        if forecast_data:
            display_weekly_forecast(city, forecast_data)

    if st.button("Тижневий графік температур"):
        forecast_data = get_weekly_forecast(api_key, city)
        if forecast_data:
            display_weekly_temperature_chart(city, forecast_data)

    if st.button("Оновити погоду"):
        st.experimental_rerun()


if __name__ == "__main__":
    main()