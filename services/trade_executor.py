import time
from services.binance_api import BinanceAPI
from config.config import TARGET_PROFIT
from utils.logger import log_info

class TradeExecutor:
    def __init__(self):
        self.api = BinanceAPI()

    def monitor_and_sell(self, symbol, buy_price, quantity):
        while True:
            current_price = float(self.api.get_24h_ticker(symbol)["lastPrice"])
            profit_percent = ((current_price - buy_price) / buy_price) * 100
            
            if profit_percent >= TARGET_PROFIT:
                self.api.place_market_order(symbol, "SELL", quantity)
                log_info(f"📈 {symbol} 매도 완료 - 수익률: {profit_percent:.2f}% | 매도가: {current_price} USDT")
                break
            
            time.sleep(10)  # 10초마다 가격 확인
