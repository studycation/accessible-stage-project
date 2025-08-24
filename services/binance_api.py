from binance.client import Client
from config.config import API_KEY, API_SECRET

class BinanceAPI:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET)

    def get_exchange_info(self):
        """모든 선물 종목의 거래 정보를 가져옴"""
        return self.client.futures_exchange_info()

    def get_24h_ticker(self, symbol):
        """24시간 동안의 가격 변동 데이터를 가져옴"""
        return self.client.futures_ticker(symbol=symbol)

    def get_min_trade_quantity(self, symbol):
        """해당 심볼의 최소 거래 가능 수량과 precision(소수점 자리수) 반환"""
        exchange_info = self.get_exchange_info()
        for s in exchange_info["symbols"]:
            if s["symbol"] == symbol:
                for f in s["filters"]:
                    if f["filterType"] == "LOT_SIZE":
                        min_qty = float(f["minQty"])
                        precision = self.get_precision(f["minQty"])
                        return min_qty, precision
        return None, None  # 최소 거래 수량을 찾지 못한 경우

    def get_precision(self, min_qty_str):
        """LOT_SIZE에서 허용하는 소수점 자리수 반환"""
        min_qty_str = str(min_qty_str)
        if "1" in min_qty_str:
            return max(0, len(min_qty_str.split(".")[-1].rstrip("0")))
        return 0  # 정수 단위 거래일 경우 (소수점 없음)

    def set_isolated_margin(self, symbol, leverage=15):
        """Isolated 모드로 설정 및 레버리지 적용 (이미 설정되어 있으면 변경하지 않음)"""
        try:
            # 현재 마진 모드 조회
            account_info = self.client.futures_account()
            for position in account_info['positions']:
                if position['symbol'] == symbol:
                    if position['isolated']:
                        return  

            # 마진 모드 변경 (필요한 경우만)
            self.client.futures_change_margin_type(symbol=symbol, marginType="ISOLATED")
        except Exception as e:
            if "No need to change margin type" in str(e):
                pass  # 이미 설정된 경우 오류 무시
            else:
                raise e  # 다른 오류는 그대로 발생시키기

        # 레버리지 설정 (항상 적용)
        self.client.futures_change_leverage(symbol=symbol, leverage=leverage)

    def place_short_order(self, symbol, quantity, entry_price):
        """숏 포지션 진입 (매도 주문), 최소 주문 금액(5 USDT) 미만이면 수량 조정"""
        min_qty, precision = self.get_min_trade_quantity(symbol)

        if precision is not None:
            quantity = round(quantity, precision)

        # 최소 주문 금액(5 USDT) 충족 검사
        min_order_value = 5  # Binance 최소 주문 금액
        if quantity * entry_price < min_order_value:
            quantity = min_order_value / entry_price
            quantity = round(quantity, precision)

        order = self.client.futures_create_order(
            symbol=symbol,
            side="SELL",  # 숏 포지션 진입
            type="MARKET",
            quantity=quantity
        )
        return order

    def place_tp_order(self, symbol, quantity, entry_price, leverage=15, target_profit=1.6):
        """PnL 기준 1.6% 수익 도달 시 자동 매도 주문 실행"""

        # PnL(수익률) 기준 목표가 계산
        target_pnl = target_profit / 100  # 예: 1.6% → 0.016
        target_price = entry_price * (1 - (target_pnl / leverage))  # PnL 기준 목표가 조정

        # 최소 주문 수량 및 Precision 확인
        min_qty, precision = self.get_min_trade_quantity(symbol)
        price_precision = self.get_price_precision(symbol)

        if precision is not None:
            quantity = round(quantity, precision)  # 주문 수량을 허용된 Precision으로 반올림

        if price_precision is not None:
            target_price = round(target_price, price_precision)  # 목표 가격도 허용된 Precision으로 반올림

        # 최소 주문 금액(5 USDT) 충족 검사
        min_order_value = 5  # Binance 최소 주문 금액
        if quantity * target_price < min_order_value:
            quantity = min_order_value / target_price
            quantity = round(quantity, precision)

        order = self.client.futures_create_order(
            symbol=symbol,
            side="BUY",  # 숏 포지션이므로 자동 매도 주문 (BUY)
            type="TAKE_PROFIT_MARKET",  # 목표가 도달 시 시장가 매도
            quantity=quantity,
            stopPrice=target_price,  # 목표가 반올림 적용
            timeInForce="GTC"
        )
        return order

    def get_price_precision(self, symbol):
        """Binance에서 허용하는 가격 Precision을 가져오는 함수"""
        exchange_info = self.get_exchange_info()
        for s in exchange_info["symbols"]:
            if s["symbol"] == symbol:
                for f in s["filters"]:
                    if f["filterType"] == "PRICE_FILTER":
                        return len(str(f["tickSize"]).rstrip('0').split('.')[-1])  # 허용된 소수점 자리수 반환
        return None


