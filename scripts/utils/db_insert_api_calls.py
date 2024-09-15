import os
import sys
import json
from mysql.connector import Error

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.utils.logger_config import get_logger # noqa: E402
from scripts.utils.db_connection import get_db_connection, close_connection  # noqa: E402

# Initialize logger for this script
logger = get_logger(os.path.basename(__file__))

def insert_api_response(script_path, payload, response, custom_params=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Convert payload and response to JSON strings
        payload_json = json.dumps(payload)
        response_json = json.dumps(response)
        
        # Prepare the SQL query
        if custom_params is not None:
            query = """
            INSERT INTO api_calls (script_path, custom_params, payload, response) 
            VALUES (%s, %s, %s, %s)
            """
            params = (script_path, custom_params, payload_json, response_json)
        else:
            query = """
            INSERT INTO api_calls (script_path, payload, response) 
            VALUES (%s, %s, %s)
            """
            params = (script_path, payload_json, response_json)

        # Execute the query
        cursor.execute(query, params)

        # Commit the transaction
        conn.commit()

        logger.info(f"Successfully inserted data for API: {script_path}")

    except Error as e:
        logger.error(f"Failed to insert data for API {script_path}. Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        close_connection(conn)

# Example usage
if __name__ == "__main__":
    try:
        # Example data
        script_path = "/path/to/api_script.py"
        payload = {"param1": "value1", "param2": "value2"}
        response = {"status": "success", "data": {"key": "value"}}
        custom_params = "param1=value1&param2=value2"  # Optional
        
        # Call with custom_params
        insert_api_response(script_path, payload, response, custom_params)
        
        # Call without custom_params
        insert_api_response(script_path, payload, response)

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")