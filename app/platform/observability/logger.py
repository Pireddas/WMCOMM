# app\platform\observability\logger.py

import logging, os
from app.application.config import settings

class FastLog:

    @staticmethod
    def write_info(name, message):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if not logger.handlers:
            log_path = os.path.join(
                settings.API_LOG_DIR,
                settings.API_LOG_INFO
            )
            handler = logging.FileHandler(log_path)
            handler.setLevel(logging.INFO)
            handler.setFormatter(
                logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            )
            logger.addHandler(handler)

        logger.info(message)
        return message

    @staticmethod
    def write_debug(name, message):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        if not logger.handlers:
            log_path = os.path.join(
                settings.API_LOG_DIR,
                settings.API_LOG_DEBUG
            )
            handler = logging.FileHandler(log_path)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(
                logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            )
            logger.addHandler(handler)

        logger.debug(message)
        return message
    
    @staticmethod
    def write_error(name, message):
        logger = logging.getLogger(name)
        logger.setLevel(logging.ERROR)
        logger.propagate = False

        if not logger.handlers:
            log_path = os.path.join(
                settings.API_LOG_DIR,
                settings.API_LOG_ERROR
            )
            handler = logging.FileHandler(log_path)
            handler.setLevel(logging.ERROR)
            handler.setFormatter(
                logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            )
            logger.addHandler(handler)
        
        message_str = " | ".join(
            f"{k}: {v}" for k, v in message.items()
        )
        logger.error(message_str)
        return message

            
    # def write_warning(name, message):
    #     logger = logging.getLogger(name)
    #     log_path = os.path.join(
    #         settings.API_LOG_DIR,
    #         settings.API_LOG_WARNING
    #     )
    #     logger.setLevel(logging.WARNING)
    #     handler = logging.FileHandler(log_path)
    #     handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    #     logger.addHandler(handler)
    #     logger.warning(message) 

    # def write_critical(name, message):
    #     logger = logging.getLogger(name)
    #     log_path = os.path.join(
    #         settings.API_LOG_DIR,
    #         settings.API_LOG_CRITICAL
    #     )
    #     logger.setLevel(logging.CRITICAL)
    #     handler = logging.FileHandler(log_path)
    #     handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    #     logger.addHandler(handler)
    #     logger.critical(message) 