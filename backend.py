import requests

API_KEY = "28c4aaa499ca148dc63af66247d21be4"


def get_data(place: str, forecast_days: int) -> []:
    """
    Get weather data from openWeatherMap.org for the specified city (place):

    Forecasts are done every 3 hours, so there are 8 per day. This API
    returns exactly 5 days worth of forecasts (i.e., 8 x 5 = 40 forecasts).
    Reduce the number of forecasts to the number of forecast_days passed
    to this function (i.e., if forecast days=1, keep 8 forecasts; if
    forecast_days=2, keep 16 forecasts; ...; if forecast_days=5, keep all 40.)

    Return the list of forecasts (where each forecast is a dictionary).

    :param place: Name of a city.
    :param forecast_days: 1 to 5 (int).
    :return: List of forecast dictionaries.
             If an error occurs, return an empty list.
    """
    # Format of API call:
    # api.openweathermap.org/data/2.5/forecast?q={city_NAME}&appid={API key}

    # Note: This site returns temperature in degrees Kelvin by default (i.e., units=standard).
    #       To get units in Centigrade, pass "units=metric".
    #       To get units in Fahrenheit, pass "units=imperial".

    url = f"https://api.openWeatherMap.org/data/2.5/forecast?q={place}&units=imperial&appid={API_KEY}"

    response = requests.get(url)
    data = response.json()

    filtered_data = []
    if data['cod'] == '200':
        if data['list']:
            filtered_data = data["list"]
            # filtered_data contains 40 dictionaries (i.e., weather samplings every 3 hours;
            # = 8 samplings/day x 5 days = 40 samplings).

            # Only keep as much data as user requested (e.g., 1 day=8 values, 2 days=16 values, etc.)
            nr_values = 8 * forecast_days
            filtered_data = filtered_data[:nr_values]  # filtered_data is a list of dictionaries.

    return filtered_data


if __name__ == '__main__':
    print(get_data("Tokyo", forecast_days=3))
    print(get_data("London", forecast_days=2))
