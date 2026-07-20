from typing import Optional
from langchain_community.llms import Ollama
from src.config import config
from src.utils.logger import setup_logger

logger = setup_logger("llm_interface")

class LocalLLM:
    """
    An Object-Oriented wrapper class interfacing with the local Ollama LLM instance
    via the LangChain orchestration framework.
    """
    
    def __init__(self):
        """
        Initializes the LLM connection wrapper using parameters pulled from
        the global system configurations ecosystem.
        """
        self.model_name = config.ollama_model
        self.base_url = config.ollama_base_url
        self.llm: Optional[Ollama] = None
        self._initialize_llm()

    def _initialize_llm(self) -> None:
        """
        Internal initialization method to construct the LangChain Ollama instance object safely.
        """
        try:
            logger.info(f"Connecting to local LLM Engine engine... Model: '{self.model_name}' | Host: {self.base_url}")
            self.llm = Ollama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.0  # Zero out randomness for factual analytics reasoning consistency
            )
            logger.info("Local LLM client structure successfully initialized.")
        except Exception as e:
            logger.exception(f"Fatal Initialization Error encountered while setting up Ollama LLM: {str(e)}")
            self.llm = None

    def query_llm(self, prompt: str) -> str:
        """
        Passes a structural instruction string prompt directly to the local model and extracts its answer text.
        
        Args:
            prompt (str): Full prompt string text containing target data context and user inquiry.
            
        Returns:
            str: The structural text generation output returned by the model.
        """
        if not self.llm:
            logger.error("LLM Execution Failure: LangChain client connector instance is uninitialized.")
            return "Error: Local AI execution client connection is unavailable."
            
        try:
            logger.info("Streaming prompt tracking context over to local model pipeline processing...")
            # Use invoke pattern consistent with latest updated LangChain framework standards
            response = self.llm.invoke(prompt)
            logger.info("Successfully received inference payload from local LLM engine.")
            return str(response).strip()
            
        except Exception as e:
            logger.exception(f"Exception encountered during LLM inference execution runtime: {str(e)}")
            return f"An operational error occurred while processing the request locally: {str(e)}"