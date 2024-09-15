import sys
import os
from mysql.connector import Error, pooling
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.utils.logger_config import get_logger # noqa: E402

# Initialize logger for this script
logger = get_logger(os.path.basename(__file__))

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),  # Default to 3306 if not specified
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB")
}

# Initialize the connection pool
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        pool_reset_session=True,
        **DB_CONFIG
    )
    logger.info("Connection pool created successfully")
except Error as e:
    logger.error(f"Error creating connection pool: {e}")
    raise

def get_db_connection():
    """
    Get a connection from the pool.
    
    Returns:
        mysql.connector.connection.MySQLConnection: A database connection object
    
    Raises:
        Error: If unable to get a connection from the pool
    """
    try:
        connection = connection_pool.get_connection()
        logger.debug("Successfully acquired a connection from the pool")
        return connection
    except Error as e:
        logger.error(f"Error getting connection from pool: {e}")
        raise

def close_connection(connection):
    """
    Close the given database connection.
    
    Args:
        connection (mysql.connector.connection.MySQLConnection): The connection to close
    """
    if connection:
        try:
            connection.close()
            logger.debug("Connection closed and returned to the pool")
        except Error as e:
            logger.error(f"Error closing connection: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Get a connection from the pool
        conn = get_db_connection()
        
        # Use the connection (example query)
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            logger.info(f"Test query result: {result}")
        
    except Error as e:
        logger.error(f"Error in database operation: {e}")
    finally:
        # Always close the connection when done
        close_connection(conn)