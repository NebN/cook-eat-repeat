from datetime import datetime, date


def date_to_string(d):
  return d.isoformat()


def string_to_datetime(d):
  return datetime.fromisoformat(d)



def string_to_date(d):
  return date.fromisoformat(d)