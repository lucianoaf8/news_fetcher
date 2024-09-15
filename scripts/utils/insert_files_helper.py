# scripts\utils\insert_files_helper.py

import os
import sys
import json

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.utils.process_fetched_data import process_and_insert_newsdata
from scripts.utils.logger_config import get_logger

# Initialize logger
logger = get_logger('insert_files_helper')

# Set the root folder path
project_root = r"C:\Projects\news_fetcher\fetched_news"

def load_and_insert_newsdata_files(root_folder):
    """
    Load all 'newsdata_data.json' files from the root folder (and subfolders) and insert them into the newsdata table.
    
    Args:
        root_folder (str): The root folder where the 'newsdata_data.json' files are stored.
    """
    try:
        # Walk through the root folder and all subfolders
        for subdir, _, files in os.walk(root_folder):
            for file in files:
                # We're only interested in 'newsdata_data.json' files
                if file.startswith("newsdata") and file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    
                    logger.info(f"Processing file: {file_path}")
                    try:
                        # Load the file content
                        with open(file_path, 'r') as f:
                            raw_content = f.read()
                            logger.debug(f"Raw content from {file_path}: {raw_content[:500]}...")  # Log the first 500 characters for debugging
                            
                            # Attempt to parse the JSON content
                            newsdata_content = json.loads(raw_content)
                            logger.debug(f"Parsed JSON content from {file_path}: {newsdata_content}")

                            # Check if JSON content is valid
                            if not newsdata_content or not isinstance(newsdata_content, dict):
                                logger.error(f"Invalid or empty JSON content in {file_path}")
                                continue

                            # Process and insert the newsdata content into the database
                            if process_and_insert_newsdata(newsdata_content):
                                logger.info(f"Successfully inserted data from {file_path} into the database.")
                            else:
                                logger.error(f"Failed to insert data from {file_path} into the database.")
                    
                    except json.JSONDecodeError as json_error:
                        logger.error(f"Failed to decode JSON from {file_path}: {str(json_error)}")
                    except Exception as e:
                        logger.error(f"Error processing file {file_path}: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error during file processing: {str(e)}")

if __name__ == "__main__":
    load_and_insert_newsdata_files(project_root)