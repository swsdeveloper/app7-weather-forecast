import pandas as pd


def get_data(days) -> ():
    """
    Get weather data (for now from hardcode)

    :param days: 1 to 5 (int)
    :return: tuple containing 2 lists. Each list will have `days + 1` number of items.
             (The +1 is for prepending today's date and temperature)
             list of dates (format:  "yyyy-mm-dd")
             list of temperatures (ints)
    """
    # Create temporary data for Plotly:
    today = "2024-05-16"
    today_temp = 13
    dates = [today, "2024-05-17", "2024-05-18", "2024-05-19", "2024-05-20", "2024-05-21"][:days+1]
    temperatures = [today_temp, 10, 11, 14, 12, 11][:days+1]
    temperatures = [days * i for i in temperatures]
    return dates, temperatures

