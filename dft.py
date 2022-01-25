import datetime


def is_date_range_valid(from_d, to_d):
    if from_d != [] and to_d != []:
        d1 = datetime.datetime(from_d[0], from_d[1], from_d[2], from_d[3], from_d[4], from_d[5])
        d2 = datetime.datetime(to_d[0], to_d[1], to_d[2], to_d[3], to_d[4], to_d[5])
        return d1 < d2
    else:
        return False


def is_in_date_range(from_d, date, to_d):
    if from_d is list and to_d is list:
        from_d = datetime.datetime(from_d[0], from_d[1], from_d[2], from_d[3], from_d[4], from_d[5])
        to_d = datetime.datetime(to_d[0], to_d[1], to_d[2], to_d[3], to_d[4], to_d[5])
    return from_d <= date <= to_d


def to_date_format(year, month, day, hours=0, mins=0, secs=0):
    return datetime.datetime(int(year), int(month), int(day), hours, mins, secs)