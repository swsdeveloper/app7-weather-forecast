import streamlit as st
import plotly.express as px
from backend import get_data

images = {
    "Clear": "images/clear.png",
    "Clouds": "images/cloud.png",
    "Rain": "images/rain.png",
    "Snow": "images/snow.png",
    }

st.set_page_config(layout="wide")

# Add title, text_input (=place), slider (=days), and selectBox (=choice)
st.title("Weather Forecast for the Next Days")

place = st.text_input("Place:")
days = st.slider('Forecast Days', min_value=1, max_value=5,
                 help="Select the number of forecasted days")
choice = st.selectbox("Select data to view", options=("Temperature", "Sky"))

# Add subheader
period = f"{days} days"
if days == 1:
    period = "day"

if place:
    st.subheader(f"{choice} for the next {period} in {place.title()}")

    # Get Temperature or Sky data (as a list of dictionaries)
    filtered_data = get_data(place, forecast_days=days)

    if filtered_data:
        # Get list of dates
        dates = [dt_dict["dt_txt"] for dt_dict in filtered_data]

        # For Temperature:
        # Each filtered_data dictionary contains a dictionary with key "main".
        # Each "main" dictionary contains a key "temp".

        if choice == "Temperature":
            # Reduce filtered_data to a list of temperatures (rounded to nearest even number).
            temperatures_f = [round(fd_dict["main"]["temp"]) for fd_dict in filtered_data]  # Fahrenheit (see backend.py)
            # Get list of dates
            dates = [dt_dict["dt_txt"] for dt_dict in filtered_data]
            # Display a line graph.
            figure = px.line(x=dates, y=temperatures_f, labels={"x": "Dates", "y": "Temperature (F)"})
            st.plotly_chart(figure, use_container_width=True)

        # For Sky:
        # Each filtered_data dictionary contains a list with key "weather".
        # That list contains 1 dictionary.
        # That inner dictionary has a key "main" which returns "Clear" or "Clouds", etc.

        elif choice == "Sky":
            # Reduce filtered_data to a list of weather conditions (strings).
            sky_conditions = [fd_dict["weather"][0]["main"] for fd_dict in filtered_data]
            # Convert the strings into image paths.
            sky_images = [images[condition] for condition in sky_conditions]
            # Display the list of images.
            st.image(sky_images, caption=sky_conditions, width=150)

        else:
            st.error("*** Invalid Choice ***")

    else:
        st.error("*** Error: Place not recognized. ***")
