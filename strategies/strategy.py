from services.data_collector import DataCollector
from services.binance_api import BinanceAPI
from config.config import MIN_24H_VOLUME, MIN_24H_PRICE_CHANGE, MIN_USDT
from utils.logger import log_info

class TradingStrategy:
    def __init__(self):
        self.data_collector = DataCollector()
        self.api = BinanceAPI()

    def check_trade_conditions(self, symbol):
        market_data = self.data_collector.fetch_market_data(symbol)
        
        if (market_data["volume"] > MIN_24H_VOLUME and 
            market_data["price_change_percent"] > MIN_24H_PRICE_CHANGE):
            return True
        return False

    def get_min_trade_amount(self, symbol):
        """최소 거래 가능 수량 및 precision을 고려한 주문 수량 계산"""
        min_qty, precision = self.api.get_min_trade_quantity(symbol)
        current_price = float(self.api.get_24h_ticker(symbol)["lastPrice"])
        
        if min_qty is None:
            return None

        # 최소 주문 금액(5 USDT)보다 작은 경우 자동 조정
        min_usdt_value = min_qty * current_price
        if min_usdt_value < MIN_USDT:
            min_qty = MIN_USDT / current_price

        # 소수점 자리수 반영
        return round(min_qty, precision) if precision is not None else min_qty

    def execute_trade(self, symbol):
        quantity = self.get_min_trade_amount(symbol)
        if quantity is not None and self.check_trade_conditions(symbol):
            self.api.set_isolated_margin(symbol)  # Isolated 15x 설정
            entry_price = float(self.api.get_24h_ticker(symbol)["lastPrice"])  # 진입 가격 가져오기

            self.api.place_short_order(symbol, quantity, entry_price)  # entry_price 추가
            log_info(f"✅ {symbol} 숏 포지션 진입 완료 - 수량: {quantity} | 진입가: {entry_price} USDT")

            self.api.place_tp_order(symbol, quantity, entry_price)  # 자동 매도 주문 실행
            log_info(f"📌 {symbol} 자동 매도 주문 설정 완료 - 목표가: {round(entry_price * 0.984, 2)} USDT")
