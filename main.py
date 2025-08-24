# import time
# from strategies.strategy import TradingStrategy
# from services.trade_executor import TradeExecutor
# from utils.logger import log_info, log_error

# trading_strategy = TradingStrategy()
# trade_executor = TradeExecutor()

# # 모든 거래 가능한 선물 심볼 가져오기
# symbols = trading_strategy.data_collector.fetch_all_symbols()

# log_info(f"모니터링 중인 종목 수: {len(symbols)}")

# for symbol in symbols:
#     try:
#         log_info(f"모니터링 중: {symbol}")

#         if trading_strategy.check_trade_conditions(symbol):
#             buy_price = float(trading_strategy.data_collector.api.get_24h_ticker(symbol)["lastPrice"])
#             quantity = trading_strategy.get_min_trade_amount(symbol)

#             trading_strategy.execute_trade(symbol)
#             log_info(f"✅ 매수 완료: {symbol} | 수량: {quantity} | 매수가: {buy_price} USDT")

#             trade_executor.monitor_and_sell(symbol, buy_price, quantity)
#     except Exception as e:
#         log_error(f"❌ 오류 발생: {symbol} - {e}")
    
#     time.sleep(0.5)  # API 요청 속도를 조절하여 제한 방지

import time
from strategies.strategy import TradingStrategy
from utils.logger import log_info, log_error

trading_strategy = TradingStrategy()

# 모든 거래 가능한 선물 심볼 가져오기
symbols = trading_strategy.data_collector.fetch_all_symbols()

log_info(f"모니터링 중인 종목 수: {len(symbols)}")

for symbol in symbols:
    try:
        log_info(f"모니터링 중: {symbol}")

        if trading_strategy.check_trade_conditions(symbol):
            trading_strategy.execute_trade(symbol)
    except Exception as e:
        log_error(f"❌ 오류 발생: {symbol} - {e}")
    
    time.sleep(0.5)  # API 요청 속도를 조절하여 제한 방지
