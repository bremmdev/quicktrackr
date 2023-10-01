import datetime

def get_today():
    return datetime.date.today().strftime("%B %d, %Y")


def get_month_range():
    first_day = datetime.date.today().replace(day=1)
    last_day = first_day.replace(
        month=first_day.month+1) - datetime.timedelta(days=1)
    return first_day, last_day
