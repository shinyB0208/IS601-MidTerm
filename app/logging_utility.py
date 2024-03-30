import logging
import logging.config
import os

class LoggingUtility:
    @staticmethod
    def configure_logging():
        os.makedirs('logs', exist_ok=True)
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")
    
    @staticmethod
    def info(message):
        logging.info(message)
    
    @staticmethod
    def warning(message):
        logging.warning(message)
    
    @staticmethod
    def error(message):
        logging.error(message)