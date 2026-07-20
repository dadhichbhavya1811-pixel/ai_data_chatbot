import pandas as pd
import numpy as np
from typing import Dict, Any, List
from src.utils.logger import setup_logger

logger = setup_logger("eda_engine")

class EDAEngine:
    """
    An Object-Oriented analytical component designed to uncover hidden data structures,
    detect numerical anomalies (outliers), and calculate variable correlations.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the EDA engine with a polished dataset DataFrame.
        
        Args:
            df (pd.DataFrame): The cleaned DataFrame to analyze.
        """
        self.df = df

    def detect_outliers_iqr(self, target_column: str) -> Dict[str, Any]:
        """
        Applies the Interquartile Range (IQR) method to identify mathematical 
        anomalies inside a specified numerical attribute.
        
        Args:
            target_column (str): The column name to check for outliers.
            
        Returns:
            Dict[str, Any]: Detailed metrics mapping the anomaly layout profile.
        """
        try:
            if target_column not in self.df.columns:
                logger.error(f"Outlier Calculation Blocked: Column '{target_column}' missing.")
                return {"error": "Column not found"}
                
            col_data = self.df[target_column]
            if not pd.api.types.is_numeric_dtype(col_data):
                logger.warning(f"Outlier Calculation Skipped: '{target_column}' is non-numerical.")
                return {"error": "Column is not numerical"}

            # Calculate IQR boundaries
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            
            # Filter and isolate out-of-bounds metrics
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            summary = {
                "column": target_column,
                "q1": float(q1),
                "q3": float(q3),
                "iqr": float(iqr),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "outlier_count": int(outliers.count()),
                "outlier_indices": list(outliers.index)
            }
            logger.info(f"Outlier Sweep Complete for '{target_column}': Flagged {summary['outlier_count']} records.")
            return summary
            
        except Exception as e:
            logger.exception(f"Exception encountered during outlier detection workflow: {str(e)}")
            return {"error": str(e)}

    def calculate_correlation_matrix(self) -> pd.DataFrame:
        """
        Computes the Pearson correlation matrix solely across the dataset's numerical variables.
        
        Returns:
            pd.DataFrame: A symmetrical correlation matrix DataFrame.
        """
        logger.info("Calculating system-wide Pearson correlation coefficient matrices...")
        numeric_df = self.df.select_dtypes(include=['number'])
        
        if numeric_df.empty or numeric_df.shape[1] < 2:
            logger.warning("Correlation Matrix Aborted: Insufficient numerical features found (minimum 2 required).")
            return pd.DataFrame()
            
        corr_matrix = numeric_df.corr(method='pearson')
        return corr_matrix