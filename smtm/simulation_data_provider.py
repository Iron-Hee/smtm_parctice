import copy
import requests
from .date_converter import DateConverter
from .data_provider import DataProvider

class SimulationDataProvider(DataProvider):
  """
  거래소로부터 과거 데이터를 수집해서 순차적으로 제공하는 클래스
  """
  
  URL = "https://api.upbit.com/v1/candles/minutes/1"
  QUERY_STRING = {"market": "KRW-BTC"}
  
  def __init__(self):
    self.is_initialized = False
    self.data = []
    self.index = 0
  
  def initialize_simulation(self, end=None, count=100):
    """Open Api를 사용해서 데이터를 가져와서 초기화한다."""
    
    self.index = 0
    query_string = copy.deepcopy(self.QUERY_STRING)
    
    if end is not None:
      query_string["to"] = end
    
    query_string["count"] = count
    try:
      if end is not None:
        query_string["to"] = DateConverter.from_kst_to_utc_str(end) + "Z"
      query_string["count"] = count
      
      response = requests.get(self.URL, params=query_string)
      response.raise_for_status() # 4xx 또는 5xx의 http 상태 코드 수신 시 requests.exceptions.HTTPError 오류 발생시킴
      self.data = response.json()
      self.data.reverse()
      self.is_initialized = True
    except ValueError as error:
      raise UserWarning("Fail get data from server") from error
    except requests.exceptions.HTTPError as error:
      raise UserWarning("Fail get data from server") from error
    except requests.exceptions.RequestException as error:
      raise UserWarning("Fail get data from server") from error
  
  def get_info(self):
    """
    현재 거래 정보를 딕셔너리로 전달
    
    Returns: 거래 정보 딕셔너리
    {
      "market": 거래 시장 종류 BTC
      "date_time": 정보의 기준 시간
      "opening_price": 시작 거래 가격
      "high_price": 최고 거래 가격
      "low_price": 최저 거래 가격
      "closing_price": 마지막 거래 가격
      "acc_price": 단위 시간내 누적 거래 금액
      "acc_volume": 단위 시간내 누적 거래 양
    } 
    """
    now = self.index
    
    if now >= len(self.data):
      return None
    
    self.index = now + 1
    return self.__create_candle_info(self.data[now])
    
  def __create_candle_info(self, data):
    try: 
      return {
        "market": data["market"],
        "date_time": data["candler_date_time_kst"],
        "opening_price": data["opening_price"],
        "high_price": data["high_price"],
        "low_price": data["low_price"],
        "closing_price": data["closing_price"],
        "acc_price": data["candle_acc_trade_price"],
        "acc_volume": data["candle_acc_trade_volume"],
    }
    except KeyError:
      return None