import json

with open("config/credentials.json") as f:
    credentials = json.load(f)

API_KEY = credentials["API_KEY"]
API_SECRET = credentials["API_SECRET"]

# 거래 조건 설정
TRADE_PAIR = "USDT"
MIN_24H_VOLUME = 100_000  # 최소 24시간 거래량 (USDT)
MIN_24H_PRICE_CHANGE = 3.0  # 최소 24시간 가격 상승률 (3%)
MIN_1MIN_VOLUME = 10_000  # 최소 1분 거래량 (USDT)
MIN_1MIN_PRICE_CHANGE = 0.5  # 최소 1분 가격 변화율 (0.5%)
MIN_BUY_RATIO = 60.0  # 매수 비율 기준 (60%)
TARGET_PROFIT = 1.6  # 목표 수익률 (%)
MIN_USDT = 5  # 최소 매수 USDT 금액
