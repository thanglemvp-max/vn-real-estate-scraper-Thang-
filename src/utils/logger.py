import logging
import os
from datetime import datetime

def get_logger(name):
    """
    Initializes a logger that outputs to both a daily log file and the console.
    """
    # Create the 'logs' directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set log filename based on current date
    log_filename = f"{log_dir}/scraping_{datetime.now().strftime('%Y-%m-%d')}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs if the logger instance already has handlers
    if not logger.handlers:
        # Define log format: Timestamp | Module Name | Level | Message
        log_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(log_format, datefmt=date_format)

        # File Handler: Saves logs to a UTF-8 encoded file
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setFormatter(formatter)

        # Console Handler: Outputs logs to the terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger