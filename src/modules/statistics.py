import pandas as pd
from typing import Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger("statistics_engine")

class StatisticsEngine:
    """
    An Object-Oriented mathematical analysis engine designed to extract 
    metadata summaries and descriptive statistical metrics from a dataset.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the engine with a target dataset.
        
        Args:
            df (pd.DataFrame): Cleaned DataFrame for profiling.
        """
        self.df = df

    def get_dataset_metadata(self) -> Dict[str, Any]:
        """
        Extracts structural shapes, counts, and health matrix parameters.
        
        Returns:
            Dict[str, Any]: High-level metadata map.
        """
        logger.info("Extracting high-level dataset metadata profiles...")
        metadata = {
            "total_records": int(self.df.shape[0]),
            "total_attributes": int(self.df.shape[1]),
            "columns": list(self.df.columns),
            "data_types": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            "total_nulls": int(self.df.isnull().sum().sum())
        }
        return metadata

    def generate_summary_statistics(self) -> Dict[str, pd.DataFrame]:
        """
        Computes separate descriptive mathematical breakdowns for both
        numeric parameters and categorical/text-based columns.
        
        Returns:
            Dict[str, pd.DataFrame]: Map holding 'numeric' and 'categorical' summaries.
        """
        logger.info("Computing descriptive summary matrices...")
        summaries = {}
        
        # 1. Process Numerical Analytics
        numeric_df = self.df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            summaries["numeric"] = numeric_df.describe().transpose()
            logger.info("Successfully compiled numeric descriptive matrix.")
        else:
            summaries["numeric"] = pd.DataFrame()
            
        # 2. Process Categorical/Text Analytics
        categorical_df = self.df.select_dtypes(include=['object', 'category', 'string'])
        if not categorical_df.empty:
            summaries["categorical"] = categorical_df.describe().transpose()
            logger.info("Successfully compiled categorical frequency distributions.")
        else:
            summaries["categorical"] = pd.DataFrame()
            
        return summaries