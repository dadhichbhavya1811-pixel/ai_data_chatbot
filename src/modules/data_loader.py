import pandas as pd
import os
from src.utils.logger import setup_logger

logger = setup_logger("data_loader")

class DataLoader:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def load_data(self, file_source=None):
        """
        Loads CSV or Excel data into a Pandas DataFrame.
        Supports both string file paths and Streamlit UploadedFile objects.
        """
        source = file_source if file_source is not None else self.file_path

        if source is None:
            raise ValueError("No file path or file object provided to DataLoader.")

        try:
            # Case 1: Source is a string file path
            if isinstance(source, str):
                if not os.path.exists(source):
                    raise FileNotFoundError(f"File not found: {source}")
                
                if source.endswith('.csv'):
                    df = pd.read_csv(source)
                elif source.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(source)
                else:
                    raise ValueError("Unsupported file format. Please upload CSV or Excel.")

            # Case 2: Source is a Streamlit UploadedFile object (or similar file buffer)
            else:
                filename = getattr(source, 'name', '').lower()
                if filename.endswith('.csv'):
                    df = pd.read_csv(source)
                elif filename.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(source)
                else:
                    # Default attempt with CSV if filename extension isn't detected
                    try:
                        df = pd.read_csv(source)
                    except Exception:
                        source.seek(0)
                        df = pd.read_excel(source)

            logger.info(f"Successfully loaded dataset with shape {df.shape}")
            return df

        except Exception as e:
            logger.error(f"Fatal System Exception encountered during data load execution: {str(e)}")
            raise e