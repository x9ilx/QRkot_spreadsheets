from datetime import timedelta


def convert_seconds_to_dhms(seconds: int) -> str:
    time_td = timedelta(seconds=seconds)
    days = time_td.days
    hours = time_td.seconds // 3600
    minutes = (time_td.seconds % 3600) // 60
    seconds = time_td.seconds % 60
    return f'{days} days {hours}:{minutes}:{seconds}'
