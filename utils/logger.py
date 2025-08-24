import logging

# 로깅 설정
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()  # 콘솔에 출력
    ]
)

def log_info(message):
    """INFO 레벨 로그 출력"""
    logging.info(message)

def log_error(message):
    """ERROR 레벨 로그 출력"""
    logging.error(message)
