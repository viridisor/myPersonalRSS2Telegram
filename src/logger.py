import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger(name):
    """
    通用日志获取函数
    支持：控制台彩色输出 + 文件滚动记录 (防止单个日志文件过大)
    """
    logger = logging.getLogger(name)

    # 如果已经配置过，直接返回，避免重复打印日志
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # 1. 创建日志目录 (项目根目录下)
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'crawler.log')

    # 2. 定义统一格式 (包含时间、级别、线程名、文件名、行号)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s:%(lineno)d - %(message)s'
    )

    # 3. 文件处理器：配置滚动，每个文件 5MB，保留 5 个备份
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # 4. 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger