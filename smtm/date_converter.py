from datetime import datetime
from datetime import timedelta

class DateConverter:
  ISO_DATEFORMAT = "%Y-%m-%dT%H:%M:%S"
  
  @classmethod
  def from_kst_to_utc_str(cls, datetime_str):
    """%Y-%m-%dT%H:%M:%S 형태의 문자열에서 9시간 뺀 문자열 반환"""
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
    dt = dt - timedelta(hours=9)
    return dt.strftime(cls.ISO_DATEFORMAT)