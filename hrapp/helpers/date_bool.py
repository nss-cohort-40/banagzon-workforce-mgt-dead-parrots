import datetime as dt

def date_bool(str):
    current_date = dt.date.today()
    start_date = dt.datetime.strptime(str, '%Y-%m-%d').date()
    return current_date < start_date