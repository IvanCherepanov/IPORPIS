import logging
import sys

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',  # Синий
        'INFO': '\033[92m',   # Зеленый
        'WARNING': '\033[93m', # Желтый
        'ERROR': '\033[91m',   # Красный
        'CRITICAL': '\033[95m' # Магента
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{log_color}{record.msg}{self.RESET}"
        return super().format(record)

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s")

logger = logging.getLogger(__name__)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColoredFormatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s"))
logger.addHandler(handler)
