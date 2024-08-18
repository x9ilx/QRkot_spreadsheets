from datetime import timedelta

MINUTES_PER_HOUR = 60
SECONDS_PER_HOUR = 3600


def convert_seconds_to_dhms(seconds: int) -> str:
    time_td = timedelta(seconds=seconds)
    days = time_td.days
    hours = time_td.seconds // SECONDS_PER_HOUR
    minutes = (time_td.seconds % SECONDS_PER_HOUR) // MINUTES_PER_HOUR
    seconds = time_td.seconds % MINUTES_PER_HOUR
    return f'{days} days {hours}:{minutes}:{seconds}'
