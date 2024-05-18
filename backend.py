import requests

API_KEY = "28c4aaa499ca148dc63af66247d21be4"


def get_data(place: str, forecast_days: int, kind: str) -> ():
    """
    Get weather data from openWeatherMap.org:

    If kind is "Temperature", returns a list of average temperatures for the
    specified number of forecast_days in the specified city (place).

    If kind is "Sky", returns a list of cloud conditions for the specified number
    of forecast_days in the specified city (place).

    If kind is invalid, returns an empty list.

    :param place: Name of a city.
    :param forecast_days: 1 to 5 (int).
    :param kind: either "Temperature" or "Sky" (the type of data to get).
    :return: tuple containing 2 lists. Each list will have `days + 1` number of items.
             (The +1 is for prepending today's date and temperature)
             list of dates (format:  "yyyy-mm-dd")
             list of temperatures (ints)
    """
    # Create temporary data for Plotly:
    # ---------------------------------
    # today = "2024-05-16"
    # today_temp = 13
    # dates = [today, "2024-05-17", "2024-05-18", "2024-05-19", "2024-05-20", "2024-05-21"][:days+1]
    # temperatures = [today_temp, 10, 11, 14, 12, 11][:forecast_days + 1]
    # temperatures = [forecast_days * i for i in temperatures]
    # return dates, temperatures

    # Format of API call:
    # api.openweathermap.org/data/2.5/forecast?Q={city_NAME}&appid={API key}

    url = f"https://www.openWeatherMap.org/data/2.5/forecast?q={place}&appid={API_KEY}"

    response = requests.get(url)
    data = response.json()

    filtered_data = {}
    if data['cod'] == 200:
        if data["list"]:
            filtered_data = data["list"]
            # filtered_data contains 40 dictionaries (i.e., weather samplings every 3 hours;
            # = 8 samplings/day x 5 days = 40 samplings).

            # Only keep as much data as user requested (e.g., 1 day=8 values, 2 days=16 values, etc.)
            nr_values = 8 * forecast_days
            filtered_data = filtered_data[:nr_values]  # filtered_data is a list of dictionaries.

            # For Temperature:
            # Each filtered_data dictionary contains a dictionary with key "main".
            # Each "main" dictionary contains a key "temp".

            # For Sky:
            # Each filtered_data dictionary contains a dictionary (fd_dict) with key "weather".
            # The value of "weather" is a list of weather conditions (weather_list).
            # The weather_list holds 1 or more dictionaries, but we only want the 1st one.
            # That dictionary has a key "main" which indicates "Clear" or "Clouds", etc.

            if kind == "Temperature":
                # Convert filtered_data to a list of temperatures.
                filtered_data = [fd_dict["main"]["temp"] for fd_dict in filtered_data]
            elif kind == "Sky":
                # Convert filtered_data to a list of weather conditions.
                weather_list = [fd_dict["weather"] for fd_dict in filtered_data]
                filtered_data = weather_list[0]["main"]
            else:
                filtered_data = []

    return filtered_data


if __name__ == '__main__':
    print(get_data("Tokyo", forecast_days=3, kind="Temperature"))
