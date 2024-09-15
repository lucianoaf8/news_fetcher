# scripts\utils\helpers.py

import os
import time
import json
import requests
from datetime import datetime
from scripts.utils.logger_config import get_logger
from scripts.utils.db_insert_api_calls import insert_api_response
from scripts.utils.track_api_calls import track_api_call
from scripts.utils.process_fetched_data import process_and_insert_data

# Initialize logger
logger = get_logger('helpers')

# Add the project root to the Python path
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


def fetch_news(url, params, api_name, api_script_path, max_retries=3):
    """
    Fetch news data from a given API.

    Args:
        url (str): API endpoint URL.
        params (dict): Parameters for the API call.
        api_name (str): Name of the API.
        api_script_path (str): Path to the specific API script file.
        max_retries (int, optional): Maximum number of retries. Defaults to 3.

    Returns:
        dict or None: JSON response from the API or None if failed.
    """
    response = None  # Initialize response
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Log the API call without the API key
            safe_params = params.copy()
            api_key_names = ['apikey', 'api_key', 'key', 'token', 'apiKey']  # Add any other possible API key parameter names
            for key in api_key_names:
                if key in safe_params:
                    safe_params[key] = '**REDACTED**'
            
            custom_params = '&'.join([f"{k}={v}" for k, v in safe_params.items()])
            insert_api_response(api_script_path, safe_params, data, custom_params)

            # Track the API call
            track_api_call(api_name)

            # NEW: Process and insert data into the database
            if not process_and_insert_data(api_name, data):
                logger.error(f"Failed to insert data from {api_name} into the database.")
            else:
                logger.info(f"Data from {api_name} successfully inserted into the database.")

            logger.info(f"Successfully fetched data from {api_name}")
            return data
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed for {api_name}: {str(e)}")
            if response is not None:
                logger.error(f"Request URL: {response.url}")  # Log the full URL for debugging
                try:
                    error_content = response.json()
                    logger.error(f"Error Content: {error_content}")
                except ValueError:
                    logger.error(f"Response content is not JSON: {response.text}")
            else:
                logger.error("No response received from the server.")
            if attempt == max_retries - 1:
                logger.error(f"Max retries reached for {api_name}. Giving up.")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff

def save_news_data(news_data):
    """
    Save the fetched news data to JSON files in a daily folder.

    Args:
        news_data (dict): Dictionary containing news data from each API.
    """
    # Get current date (for daily folder) and current time (for each file)
    date_str = datetime.now().strftime('%Y%m%d')
    time_str = datetime.now().strftime('%H%M%S')
    
    # Create a daily folder based on the date
    folder_path = os.path.join(project_root, 'fetched_news', date_str)
    os.makedirs(folder_path, exist_ok=True)

    # Save each API data file with a timestamp in the filename
    for api_name, api_data in news_data.items():
        filename = f'{api_name}_{time_str}.json'
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'w') as f:
            json.dump(api_data, f, indent=4)

        logger.info(f"{api_name} data saved to {file_path}")