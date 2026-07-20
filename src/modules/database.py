import os
import sqlite3
import pandas as pd
from typing import Optional, List
from src.utils.logger import setup_logger

logger = setup_logger("database_manager")

class DatabaseManager:
    """
    An Object-Oriented local storage repository wrapper that leverages SQLite3 
    to cache, fetch, and maintain structured data frames locally.
    """
    
    def __init__(self, db_name: str = "data/chatbot_storage.db"):
        """
        Initializes the manager with a target SQLite database file location.
        
        Args:
            db_name (str): Relative or absolute path to the database file.
        """
        self.db_name = db_name
        # Ensure the destination directory path physically exists
        db_dir = os.path.dirname(self.db_name)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def save_dataframe(self, table_name: str, df: pd.DataFrame) -> bool:
        """
        Saves or overwrites a Pandas DataFrame as a relational SQL table.
        
        Args:
            table_name (str): Name of the SQL table target.
            df (pd.DataFrame): The DataFrame to write.
            
        Returns:
            bool: True if writing succeeded, else False.
        """
        try:
            logger.info(f"Writing DataFrame records to local SQL table: '{table_name}'...")
            
            # Open formal SQL network/file context block
            with sqlite3.connect(self.db_name) as conn:
                df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
                
            logger.info(f"Database Write Complete: Table '{table_name}' successfully updated.")
            return True
        except Exception as e:
            logger.exception(f"Exception encountered during SQL write execution: {str(e)}")
            return False

    def load_dataframe(self, table_name: str) -> Optional[pd.DataFrame]:
        """
        Queries a local SQLite table directly back into a usable Pandas DataFrame.
        
        Args:
            table_name (str): The target SQL table name to load.
            
        Returns:
            Optional[pd.DataFrame]: Populated DataFrame if found, else None.
        """
        try:
            logger.info(f"Querying storage records from local SQL table: '{table_name}'...")
            
            with sqlite3.connect(self.db_name) as conn:
                # First check if the targeted table name exists inside the master schema
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?", 
                    (table_name,)
                )
                if not cursor.fetchone():
                    logger.warning(f"Database Query Blocked: Table '{table_name}' does not exist.")
                    return None
                
                # Fetch full contents back into workspace memory
                df = pd.read_sql_query(f"SELECT * FROM [{table_name}]", conn)
                
            logger.info(f"Database Read Complete: Extracted {df.shape[0]} rows from '{table_name}'.")
            return df
        except Exception as e:
            logger.exception(f"Exception encountered during SQL read execution: {str(e)}")
            return None

    def get_all_tables(self) -> List[str]:
        """
        Scans the master SQLite database schema to return all saved table names.
        
        Returns:
            List[str]: A list of all active tables in storage.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
            return tables
        except Exception as e:
            logger.error(f"Failed to extract master table schema list: {str(e)}")
            return []