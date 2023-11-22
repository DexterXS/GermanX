import streamlit as st
import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()
            return data
        except requests.exceptions.HTTPError as errh:
            st.exception(f"HTTP Error: {errh}")
            return None
        except requests.exceptions.RequestException as err:
            st.exception(f"Request Exception: {err}")
            return None
        except requests.exceptions.JSONDecodeError as err:
            st.exception(f"JSON Decode Error: {err}")
            st.exception(f"Response Text: {response.text}")
            return None

st.title("Погодний додаток")

city = st.text_input("Введіть місто:", "Kyiv")

api_key = "c6c8f1d7c5a3cb77f9213311afb839d3"

weather_api = WeatherAPI(api_key=api_key)

weather_data = weather_api.get_weather(city)
if weather_data:
    temperature = weather_data["main"]["temp"]
    st.write(f"Погода у {city}: {temperature}°C")
