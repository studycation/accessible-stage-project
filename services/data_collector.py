import time
from services.binance_api import BinanceAPI

class DataCollector:
    def __init__(self):
        self.api = BinanceAPI()

    def fetch_all_symbols(self):
        """현재 거래 가능한 모든 선물 심볼을 가져옴"""
        exchange_info = self.api.get_exchange_info()
        return [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']

    def fetch_market_data(self, symbol):
        """각 심볼의 24시간 거래량과 가격 변동을 가져옴"""
        time.sleep(0.5)  # API 요청 제한을 방지하기 위해 0.5초 대기
        data = self.api.get_24h_ticker(symbol)
        return {
            "symbol": symbol,
            "price_change_percent": float(data["priceChangePercent"]),
            "volume": float(data["quoteVolume"])
        }
