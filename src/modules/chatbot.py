import pandas as pd
from typing import Optional, Dict, Any
from src.modules.statistics import StatisticsEngine
from src.modules.database import DatabaseManager
from src.modules.llm import LocalLLM
from src.modules.prompts import PromptTemplates
from src.utils.logger import setup_logger

logger = setup_logger("chatbot_orchestrator")

class ChatbotOrchestrator:
    """
    The central coordination hub that links tabular state matrices, local SQL 
    repositories, data profiling engines, and the local LLM reasoning thread.
    """
    
    def __init__(self):
        """Initializes all downstream logical processing sub-modules."""
        logger.info("Initializing central Chatbot Orchestrator pipeline...")
        self.db_manager = DatabaseManager()
        self.llm_interface = LocalLLM()
        self.current_df: Optional[pd.DataFrame] = None
        self.current_table_name: Optional[str] = None

    def set_active_dataset(self, table_name: str, df: pd.DataFrame) -> None:
        """
        Sets the active DataFrame workspace state and flushes it to the local cache database.
        
        Args:
            table_name (str): The logical storage identifier for the dataset.
            df (pd.DataFrame): The active dataset.
        """
        self.current_df = df
        self.current_table_name = table_name
        logger.info(f"Active workspace synchronized to dataset table identity: '{table_name}'")
        self.db_manager.save_dataframe(table_name, df)

    def load_dataset_from_cache(self, table_name: str) -> bool:
        """
        Attempts to reload a historically cached dataset directly out of SQL storage.
        
        Args:
            table_name (str): Target table identity to restore.
            
        Returns:
            bool: True if context restoration succeeded, else False.
        """
        cached_df = self.db_manager.load_dataframe(table_name)
        if cached_df is not None:
            self.current_df = cached_df
            self.current_table_name = table_name
            logger.info(f"Successfully restored workspace context from cached table: '{table_name}'")
            return True
        logger.warning(f"Failed to locate or restore workspace cache for table name: '{table_name}'")
        return False

    def process_user_query(self, user_query: str) -> str:
        """
        Core pipeline method that profiles the dataset state, maps context templates, 
        and extracts data science insights from the local LLM engine.
        
        Args:
            user_query (str): The natural language data question submitted by the user.
            
        Returns:
            str: Factual analytical summary text derived directly by the local AI engine.
        """
        if self.current_df is None:
            # Fallback check if workspace has no data matrix loaded
            logger.warning("Query rejected: No active dataset matrix initialized in current session state.")
            return "Please upload or select a target dataset matrix before asking data questions."

        try:
            logger.info(f"Processing query: '{user_query}' over active dataset: '{self.current_table_name}'")
            
            # 1. Compile real-time profile summaries and metrics out of the statistics module
            stats_engine = StatisticsEngine(self.current_df)
            metadata = stats_engine.get_dataset_metadata()
            summaries = stats_engine.generate_summary_statistics()
            
            # Format the descriptive matrix cleanly into string space
            numeric_summary_str = ""
            if 'numeric' in summaries and not summaries['numeric'].empty:
                numeric_summary_str = summaries['numeric'].to_string()
            else:
                numeric_summary_str = "No numerical columns available for descriptive calculation."

            # 2. Build the final prompt by injecting metadata and summaries into templates
            compiled_prompt = PromptTemplates.get_analysis_prompt(
                metadata=metadata,
                numeric_summary=numeric_summary_str,
                user_query=user_query
            )

            # 3. Stream the prompt payload straight over to the local LLM interface
            ai_response = self.llm_interface.query_llm(compiled_prompt)
            return ai_response

        except Exception as e:
            logger.exception(f"Fatal exception hit during chatbot orchestration processing: {str(e)}")
            return f"An orchestrator error occurred while processing the dataset query: {str(e)}"