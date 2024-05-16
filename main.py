import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Weather Forecast for the Next Days")

cities = ['New York', 'Rome', 'Paris']

city = st.text_input("Place:", key="city")  # , on_change=qqq)
days = st.slider('Forecast Days', min_value=1, max_value=5)

period = f"{days} days"
if days == 1:
    period = "day"

options = ["Temperature", "Weather"]
choice = st.selectbox("Select data to view", options=options)  # , on_change=qqq)

if choice == "Temperature":
    st.header(f"Temperature for the next {period} in {city}")
    # st.line_chart(x="Date", y="Temperature (C)")
else:
    st.header(f"Weather for the next {period} in {city}")

# st.session_state.city
