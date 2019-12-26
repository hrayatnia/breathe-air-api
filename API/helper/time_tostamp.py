from datetime import datetime


def to_timestamp(date):
    d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f").strftime('%s.%f')
    return int(float(d)*1000)