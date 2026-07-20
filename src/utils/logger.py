import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "ai_data_chatbot") -> logging.Logger:
    """
    Configures and returns a production-ready logger that outputs
    diagnostics to both the console and a rolling log file.
    
    Args:
        name (str): The name identifier for the logger instance.
        
    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, don't add them again
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Ensure the logs directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, "app.log")
    
    # Create structural string format for log readouts
    log_format = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File Handler - configured to roll over when file size hits 5MB, keeping 3 backups
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    
    # Console Handler for real-time visibility in Command Prompt
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    
    # Attach both handlers to the central logger engine
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger