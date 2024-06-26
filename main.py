import streamlit as st
import plotly.express as px
from backend import get_data
from datetime import datetime

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
    place_parts = place.title().split(",")  # capitalize each word
    for index, part in enumerate(place_parts):
        part = part.strip()
        if 2 <= len(part) <= 3:
            part = part.upper()  # make state code and/or country abbreviation uppercase
        place_parts[index] = part
    adjusted_place = ", ".join(place_parts)

    st.subheader(f"{choice} for the next {period} in: {adjusted_place}")

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
            # Convert date strings into datetime objects.
            date_times = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") for date_str in dates]
            # Create captions out of the datetime objects (e.g., "Mon. Jan 22  06:00 AM")
            captions = [date_time.strftime("%a. %b %d  %I:%M %p") for date_time in date_times]
            # Display the list of images and captions.
            st.image(sky_images, caption=captions, width=150)

        else:
            st.error("*** Invalid Choice ***")

    else:
        st.error("*** Error: Place not recognized. ***")
