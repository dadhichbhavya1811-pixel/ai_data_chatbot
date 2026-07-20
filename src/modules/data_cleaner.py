import pandas as pd
from typing import Optional
from src.utils.logger import setup_logger

# Initialize modular logger instance
logger = setup_logger("data_cleaner")

class DataCleaner:
    """
    An Object-Oriented pipeline component that handles automated structural cleaning,
    imputation strategies, and whitespace parsing on Pandas DataFrames.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the cleaner with a target DataFrame instance copy.
        
        Args:
            df (pd.DataFrame): The raw DataFrame requiring structural cleaning.
        """
        # Create a deep copy to avoid modifying the original source object implicitly
        self.df = df.copy()

    def remove_duplicates(self) -> int:
        """
        Identifies and purges completely duplicate rows from the dataset.
        
        Returns:
            int: The total count of duplicate rows dropped.
        """
        initial_rows = self.df.shape[0]
        self.df.drop_duplicates(inplace=True)
        dropped_count = initial_rows - self.df.shape[0]
        
        if dropped_count > 0:
            logger.info(f"Duplicate Purging: Dropped {dropped_count} redundant rows from workspace.")
        else:
            logger.info("Duplicate Purging: No redundant rows identified.")
        return dropped_count

    def clean_missing_values(self) -> pd.DataFrame:
        """
        Automatically handles missing values across features:
        - Numerical features: Imputed using statistical median values.
        - Categorical/Text features: Imputed using a placeholder flag string ('Unknown').
        
        Returns:
            pd.DataFrame: The structurally cleaned and imputed DataFrame object.
        """
        try:
            logger.info("Initiating automated structural imputation routines...")
            
            for column in self.df.columns:
                null_count = self.df[column].isnull().sum()
                if null_count == 0:
                    continue
                
                # Check data type structure for numeric fields
                if pd.api.types.is_numeric_dtype(self.df[column]):
                    median_value = self.df[column].median()
                    # Fallback check if the entire column is null
                    if pd.isnull(median_value):
                        median_value = 0
                    self.df[column] = self.df[column].fillna(median_value)
                    logger.info(f"Imputation: Column '{column}' | Filled {null_count} nulls with Median value ({median_value}).")
                
                # Treat as categorical/text features
                else:
                    self.df[column] = self.df[column].fillna("Unknown")
                    # Clean trailing whitespaces if values are text strings
                    if pd.api.types.is_object_dtype(self.df[column]) or pd.api.types.is_string_dtype(self.df[column]):
                        self.df[column] = self.df[column].astype(str).str.strip()
                    logger.info(f"Imputation: Column '{column}' | Filled {null_count} nulls with 'Unknown'.")
            
            return self.df
            
        except Exception as e:
            logger.exception(f"Fatal System Exception encountered during data cleaning execution: {str(e)}")
            raise e

    def execute_full_cleaning_pipeline(self) -> pd.DataFrame:
        """
        Orchestrates full structural cleaning processes in sequential execution order.
        
        Returns:
            pd.DataFrame: Fully polished DataFrame.
        """
        self.remove_duplicates()
        return self.clean_missing_values()