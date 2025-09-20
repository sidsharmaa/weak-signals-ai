# src/data/data_ingestion.py
import logging
import pandas as pd
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataSource(ABC):
    @abstractmethod
    def fetch_data(self) -> pd.DataFrame:
        pass

class LocalFileDataSource(DataSource):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_data(self) -> pd.DataFrame:
        """
        Reads a tab-separated (TSV) file into a pandas DataFrame, ensuring all
        columns are loaded as strings to prevent type inference errors.
        """
        logging.info(f"Reading local data from {self.file_path}...")
        try:
            # Add dtype=str to force pandas to load all columns as strings
            df = pd.read_csv(self.file_path, sep='\t', dtype=str)
            
            # You may need to adjust these names based on your file's actual columns
            df.rename(columns={'abstract': 'summary'}, inplace=True)
            
            logging.info(f"Successfully loaded {len(df)} records.")
            return df
        except FileNotFoundError:
            logging.error(f"File not found at path: {self.file_path}")
            raise
        except Exception as e:
            logging.error(f"An error occurred while reading the file: {e}")
            raise