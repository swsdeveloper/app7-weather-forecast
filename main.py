import streamlit as st
import plotly.express as px
from get_data import get_data

st.set_page_config(layout="wide")

st.title("Weather Forecast for the Next Days")

place = st.text_input("Place:")

days = st.slider('Forecast Days', min_value=1, max_value=5,
                 help="Select the number of forecasted days")

options = ["Temperature", "Sky"]
choice = st.selectbox("Select data to view", options=options)

period = f"{days} days"
if days == 1:
    period = "day"

st.subheader(f"{choice} for the next {period} in {place}")

d, t = get_data(days)

# Create a Plotly figure (line graph)
figure = px.line(x=d, y=t, labels={"x": "Dates", "y": "Temperature (C)"})
st.plotly_chart(figure, use_container_width=True)
