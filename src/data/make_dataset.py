# src/data/make_dataset.py
import os
import logging
from src.config import config
from src.data.data_ingestion import LocalFileDataSource

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting local data processing pipeline...")
    source = LocalFileDataSource(file_path=config.data.raw_path)
    
    try:
        raw_data = source.fetch_data()
    except FileNotFoundError:
        logging.error("Halting pipeline: Raw data file not found.")
        return

    output_dir = os.path.dirname(config.data.processed_path)
    os.makedirs(output_dir, exist_ok=True)
    
    raw_data.to_parquet(config.data.processed_path, index=False)
    logging.info(f"Data processing complete. Saved Parquet file to {config.data.processed_path}")

if __name__ == '__main__':
    main()