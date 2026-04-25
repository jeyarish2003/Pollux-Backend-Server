import logging
from logging.handlers import RotatingFileHandler
from pprint import pformat
import os

from common.utils.date_helper import ISTFormatter


class Logger:
    def __init__(self, log_level=logging.DEBUG, log_file="app.log", max_size=5_000_000, backup_count=5):
        """
        Initializes a Logger instance.

        Args:
          log_level (int): Logging level. Defaults to logging.DEBUG.
          log_file (str): File to write logs to. Defaults to app.log.
          max_size (int): Max file size in bytes before rotation (5MB default).
          backup_count (int): How many rotated files to keep.
        """
        self.logger = logging.getLogger("POLLUX SERVER")
        self.logger.setLevel(log_level)


        
        log_file_path = os.path.join('logs', log_file)
        
        # Prevent duplicates
        if not self.logger.handlers:
            # ===========================
            # 1️⃣ Console Handler
            # ===========================
            console_handler = logging.StreamHandler()
            formatter = ISTFormatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # formatter = logging.Formatter(
            #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            #     datefmt="%Y-%m-%d %H:%M:%S"
            # )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # ===========================
            # 2️⃣ File Handler (Rotating)
            # ===========================
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=max_size,
                backupCount=backup_count,
                encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def _format_message(self, message, *args, **kwargs):
        """Format message safely with pformat only for complex objects."""
        if args or kwargs:
            message = message.format(*args, **kwargs)

        if isinstance(message, (dict, list, tuple, set)):
            return pformat(message)

        return str(message)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(self._format_message(message, *args, **kwargs))

    def info(self, message, *args, **kwargs):
        self.logger.info(self._format_message(message, *args, **kwargs))

    def warning(self, message, *args, **kwargs):
        self.logger.warning(self._format_message(message, *args, **kwargs))

    def error(self, message, *args, **kwargs):
        self.logger.error(self._format_message(message, *args, **kwargs))

    def critical(self, message, *args, **kwargs):
        self.logger.critical(self._format_message(message, *args, **kwargs))
