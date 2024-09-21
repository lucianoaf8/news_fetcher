# C:\Projects\news_fetcher\scripts\apis\fetch_interests.py

import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.utils.db_connection import get_db_connection, close_connection
from scripts.utils.logger_config import get_logger

# Initialize logger
logger = get_logger('get_interests')

def get_interests():
    """
    Fetch interests from the database.

    Returns:
        list: A list of dictionaries containing interest data.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id, formatted_interest, category, language, country
        FROM interests
        WHERE status = 1
        AND id IN (36);
        """

        cursor.execute(query)
        interests = cursor.fetchall()

        logger.info(f"Successfully fetched {len(interests)} interests from the database")
        return interests

    except Exception as e:
        logger.error(f"Error fetching interests from database: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            close_connection(conn)

if __name__ == "__main__":
    # Test the function
    fetched_interests = get_interests()
    for interest in fetched_interests:
        print(interest)