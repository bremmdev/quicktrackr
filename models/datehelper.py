import datetime


class DateHelper:
    @classmethod
    def today(cls):
        return datetime.date.today().strftime("%B %d, %Y")

    @classmethod
    def month_range(cls):
        first_day = datetime.date.today().replace(day=1)
        last_day = first_day.replace(
            month=first_day.month+1) - datetime.timedelta(days=1)
        return first_day, last_day

    @classmethod
    def months_in_year(cls):
        current_year = datetime.datetime.now().year
        months = [{"name": datetime.date(current_year, i, 1).strftime(
            '%B'), "number": i} for i in range(1, 13)]
        return months

    @classmethod
    def current_month_year(cls):
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        return current_month, current_year
