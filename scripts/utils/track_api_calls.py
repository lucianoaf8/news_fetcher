# scripts\utils\track_api_calls.py

import os
import sys
from datetime import date, datetime
from mysql.connector import Error

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.utils.logger_config import get_logger
from scripts.utils.db_connection import get_db_connection, close_connection

# Initialize logger
logger = get_logger('track_api_calls')

def get_api_info(conn, api_name_id):
    """
    Retrieve API information from the api_info table.
    
    Args:
        conn: Database connection object
        api_name_id (str): Name of the API
    
    Returns:
        dict: API information or None if not found
    """
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM api_info WHERE api_name_id = %s"
        cursor.execute(query, (api_name_id,))
        api_info = cursor.fetchone()
        cursor.close()
        return api_info
    except Error as e:
        logger.error(f"Error retrieving API info for {api_name_id}: {e}")
        return None

def update_api_usage(conn, api_info):
    """
    Update or insert a record in the api_usage table.
    
    Args:
        conn: Database connection object
        api_info (dict): API information
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        today = date.today()
        now = datetime.now()

        # Check if there's an existing record for today
        query = """
        SELECT id, total_calls_made FROM api_usage 
        WHERE api_id = %s AND date = %s
        """
        cursor.execute(query, (api_info['id'], today))
        existing_record = cursor.fetchone()

        if existing_record:
            # Update existing record
            update_query = """
            UPDATE api_usage SET total_calls_made = %s, last_fetch = %s
            WHERE id = %s
            """
            new_total_calls = existing_record[1] + 1
            cursor.execute(update_query, (new_total_calls, now, existing_record[0]))
        else:
            # Insert new record
            insert_query = """
            INSERT INTO api_usage (api_id, api_name_id, date, last_fetch, total_calls_made)
            VALUES (%s, %s, %s, %s, 1)
            """
            cursor.execute(insert_query, (api_info['id'], api_info['api_name_id'], today, now))

        conn.commit()
        cursor.close()
        return True
    except Error as e:
        logger.error(f"Error updating API usage for {api_info['api_name_id']}: {e}")
        conn.rollback()
        return False

def track_api_call(api_name_id):
    """
    Track an API call by updating the database.
    
    Args:
        api_name_id (str): Name of the API being called
    
    Returns:
        bool: True if tracking was successful, False otherwise
    """
    conn = None
    try:
        conn = get_db_connection()
        api_info = get_api_info(conn, api_name_id)
        
        if api_info is None:
            logger.error(f"API '{api_name_id}' not found in api_info table")
            return False
        
        success = update_api_usage(conn, api_info)
        
        if success:
            logger.info(f"Successfully tracked API call for {api_name_id}")
            print(f"API call tracked: {api_name_id}")
        else:
            logger.warning(f"Failed to track API call for {api_name_id}")
            print(f"Failed to track API call: {api_name_id}")
        
        return success
    except Error as e:
        logger.error(f"Database error while tracking API call for {api_name_id}: {e}")
        print(f"Error tracking API call: {api_name_id}")
        return False
    finally:
        if conn:
            close_connection(conn)

# Example usage
if __name__ == "__main__":
    test_api_name_id = "example_api"
    result = track_api_call(test_api_name_id)
    print(f"Test tracking result: {'Successful' if result else 'Failed'}")