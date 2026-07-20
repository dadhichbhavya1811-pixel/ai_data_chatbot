import os
from dataclasses import dataclass
from dotenv import load_dotenv
from src.utils.logger import setup_logger

# Initialize logging framework for configuration validation tracking
logger = setup_logger("config_module")

# Explicitly pull variables from the local environment file
load_dotenv()

@dataclass(frozen=True)
class AppConfig:
    """
    Immutable configuration structure holding core environmental 
    settings for the local application architecture.
    """
    app_name: str = os.getenv("APP_NAME", "AI Data Chatbot")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def validate_config(self) -> bool:
        """
        Validates that critical runtime parameters are present.
        
        Returns:
            bool: True if configuration maps out securely.
        """
        if not self.ollama_base_url.startswith("http"):
            logger.error("Configuration Check Failed: OLLAMA_BASE_URL must be a valid HTTP URL.")
            return False
        logger.info("Configuration parameters safely loaded and verified.")
        return True

# Instantiate a single, global application configuration object
config = AppConfig()
config.validate_config()