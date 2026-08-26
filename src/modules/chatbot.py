import os
import pandas as pd
from typing import Optional, Dict, Any
from openai import OpenAI
import streamlit as st

from src.modules.statistics import StatisticsEngine
from src.modules.database import DatabaseManager
from src.modules.prompts import PromptTemplates
from src.utils.logger import setup_logger

logger = setup_logger("chatbot_orchestrator")

class ChatbotOrchestrator:
    """
    Central coordination hub linking tabular state matrices, local SQL 
    repositories, data profiling engines, and Groq Cloud LLM reasoning.
    """
    
    def __init__(self):
        """Initializes processing modules and connects securely to Groq's API."""
        logger.info("Initializing central Chatbot Orchestrator pipeline with Groq Cloud...")
        self.db_manager = DatabaseManager()
        
        # 1. Safely retrieve the Groq API key from Streamlit secrets or environment variables
        api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))
        
        # 2. Initialize Groq API client connection
        self.openai_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        
        # 3. Production model on Groq
        self.model = "openai/gpt-oss-120b"
        
        self.current_df: Optional[pd.DataFrame] = None
        self.current_table_name: Optional[str] = None

    def set_active_dataset(self, table_name: str, df: pd.DataFrame) -> None:
        """Sets active DataFrame workspace state and flushes to local SQL cache."""
        self.current_df = df
        self.current_table_name = table_name
        logger.info(f"Active workspace synchronized to dataset table identity: '{table_name}'")
        self.db_manager.save_dataframe(table_name, df)

    def load_dataset_from_cache(self, table_name: str) -> bool:
        """Attempts to reload a historically cached dataset directly out of SQL storage."""
        cached_df = self.db_manager.load_dataframe(table_name)
        if cached_df is not None:
            self.current_df = cached_df
            self.current_table_name = table_name
            logger.info(f"Successfully restored workspace context from cached table: '{table_name}'")
            return True
        logger.warning(f"Failed to locate workspace cache for table name: '{table_name}'")
        return False

    def process_user_query(self, user_query: str) -> str:
        """Profiles dataset state, evaluates full dataset metrics, and queries Groq Cloud LLM."""
        if self.current_df is None:
            logger.warning("Query rejected: No active dataset matrix initialized.")
            return "Please upload or select a target dataset matrix before asking data questions."

        try:
            logger.info(f"Processing query: '{user_query}' over active dataset: '{self.current_table_name}'")
            
            # 1. Extract Full Column Profiles & Value Counts across the ENTIRE dataset
            df = self.current_df
            columns_list = list(df.columns)
            total_rows = len(df)
            
            # Compute categorical value breakdowns for all categorical columns (up to 20 unique values each)
            categorical_breakdowns = {}
            for col in df.select_dtypes(include=['object', 'category', 'string']).columns:
                value_counts = df[col].value_counts(dropna=False).head(20).to_dict()
                categorical_breakdowns[col] = value_counts

            # Compute complete numerical stats across ALL rows
            numeric_stats = {}
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                numeric_stats = numeric_df.describe().to_dict()

            # 2. Build full dataset context payload
            full_context = (
                f"FULL DATASET SUMMARY & METRICS:\n"
                f"- Dataset Name: {self.current_table_name}\n"
                f"- Total Records (Exact Row Count): {total_rows}\n"
                f"- Columns: {columns_list}\n\n"
                f"EXACT CATEGORICAL VALUE COUNTS (FULL DATASET):\n{categorical_breakdowns}\n\n"
                f"NUMERICAL METRICS (FULL DATASET):\n{numeric_stats}\n\n"
                f"USER QUESTION: {user_query}"
            )

            # 3. System Prompt: Force AI to give exact figures from full statistics without writing code
            system_prompt = (
                "You are an expert Data Analyst AI with complete access to full dataset metrics and exact row tallies.\n"
                "Guidelines:\n"
                "1. Answer the user's question directly with exact counts, totals, or statistics calculated from the dataset.\n"
                "2. NEVER say 'I cannot access the full dataset' or suggest running SQL/Python queries.\n"
                "3. Do NOT output Python or SQL code. Give clear, natural-language analytical answers only."
            )

            # 4. Query Groq API
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_context}
                ],
                temperature=0.2
            )
            
            ai_response = response.choices[0].message.content
            return ai_response

        except Exception as e:
            logger.exception(f"Fatal exception during Groq query processing: {str(e)}")
            return f"An orchestrator error occurred while processing the dataset query: {str(e)}"