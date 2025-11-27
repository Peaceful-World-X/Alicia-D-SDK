import os
from datetime import datetime

from .beauty_logger import *

# 创建统一的日志文件，使用日期时间命名
# 支持通过环境变量 ALICIA_D_SDK_NO_LOG=1 禁用日志文件生成
_log_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
_disable_log = os.environ.get('ALICIA_D_SDK_NO_LOG', '0') == '1'

logger = BeautyLogger(
    log_dir="./logs",
    log_name=f"alicia_d_sdk_{_log_timestamp}.log",
    verbose=not _disable_log,  # 禁用日志时也不在控制台打印
    min_level=LogLevel.INFO,
    enable_file=not _disable_log  # 禁用日志文件写入
)
