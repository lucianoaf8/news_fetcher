# scripts\utils\process_fetched_data.py

import os
import sys
import json
from mysql.connector import Error
from scripts.utils.db_connection import get_db_connection, close_connection
from scripts.utils.logger_config import get_logger
from datetime import datetime

# Add the project root to the Python path
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

logger = get_logger('process_fetched_data')

def process_and_insert_data(api_name, api_response):
    """
    Process the API response and insert the results into the appropriate table.
    
    Args:
        api_name (str): The name of the API (e.g., 'newsdata', 'newsapi', etc.)
        api_response (dict): The JSON response from the API
    
    Returns:
        bool: True if processing and insertion were successful, False otherwise
    """
    if api_name == 'newsdata':
        return process_and_insert_newsdata(api_response)
    elif api_name == 'newsapi':
        return process_and_insert_newsapi(api_response)
    elif api_name == 'gnews':
        return process_and_insert_gnews(api_response)
    elif api_name == 'mediastack':
        return process_and_insert_mediastack(api_response)
    elif api_name == 'currentsapi':
        return process_and_insert_currentsapi(api_response)
    else:
        logger.error(f"Unsupported API: {api_name}")
        return False
    
def insert_data_into_db(data_list, table_name):
    """
    Insert data into the given table, skipping duplicate entries.
    
    Args:
        data_list (list): A list of dictionaries containing the data to be inserted.
        table_name (str): The name of the table where the data should be inserted.
    
    Returns:
        bool: True if the insertion was successful, False otherwise
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for data in data_list:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(sql, list(data.values()))
            except Error as e:
                # Check for duplicate entry error code 1062
                if e.errno == 1062:
                    logger.warning(f"Duplicate entry found: {e}, skipping this record.")
                    continue  # Skip this record and continue with the next one
                else:
                    raise  # Re-raise the exception if it's not a duplicate entry error

        conn.commit()
        logger.info(f"Successfully inserted {len(data_list)} records into {table_name} table (excluding duplicates)")
        return True

    except Error as e:
        logger.error(f"Error inserting data into {table_name} table: {e}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            close_connection(conn)


def process_and_insert_newsdata(api_response):
    """
    Process the NewsData.io API response and insert the results into the newsdata table.
    
    Args:
        api_response (dict): The JSON response from the NewsData.io API
    
    Returns:
        bool: True if processing and insertion were successful, False otherwise
    """
    if not api_response:
        logger.error("Empty API response received.")
        return False

    processed_articles = []
    for article in api_response.get('results', []):
        # Validate and log missing fields
        article_id = article.get('article_id', None)
        if not article_id:
            logger.error("Missing 'article_id' in article data.")
            continue

        title = article.get('title', 'No Title')
        link = article.get('link', 'No Link')
        
        # Prepare the data for insertion, with validation for required fields
        processed_articles.append({
            'article_id': article_id,
            'title': title,
            'link': link,
            'keywords': json.dumps(article.get('keywords', [])),
            'creator': json.dumps(article.get('creator', [])),
            'video_url': article.get('video_url', None),
            'description': article.get('description', ''),
            'content': article.get('content', ''),
            'pubDate': article.get('pubDate', None),
            'pubDateTZ': article.get('pubDateTZ', None),
            'image_url': article.get('image_url', None),
            'source_id': article.get('source_id', None),
            'source_priority': article.get('source_priority', None),
            'source_name': article.get('source_name', 'Unknown Source'),
            'source_url': article.get('source_url', None),
            'source_icon': article.get('source_icon', None),
            'language': article.get('language', None),
            'country': ','.join(article.get('country', [])),
            'category': ','.join(article.get('category', [])),
            'ai_tag': article.get('ai_tag', None),
            'sentiment': article.get('sentiment', None),
            'sentiment_stats': json.dumps(article.get('sentiment_stats', {})),
            'ai_region': article.get('ai_region', None),
            'ai_org': article.get('ai_org', None),
            'duplicate': article.get('duplicate', None)
        })

    if not processed_articles:
        logger.error("No valid articles to insert.")
        return False

    return insert_data_into_db(processed_articles, 'newsdata')

def process_and_insert_newsapi(api_response):
    """
    Process the NewsAPI response and insert the results into the newsapi table.
    
    Args:
        api_response (dict): The JSON response from the NewsAPI
    
    Returns:
        bool: True if processing and insertion were successful, False otherwise
    """
    if not api_response or 'articles' not in api_response:
        logger.error("Invalid or empty API response received.")
        return False

    processed_articles = []

    for article in api_response['articles']:
        # Extract and process the data
        source_id = article['source'].get('id')
        source_name = article['source'].get('name', 'Unknown Source')
        author = article.get('author')
        title = article.get('title', 'No Title')
        description = article.get('description')
        url = article.get('url', 'No URL')
        url_to_image = article.get('urlToImage')
        published_at = article.get('publishedAt')
        content = article.get('content')

        # Convert publishedAt to MySQL DATETIME format
        if published_at:
            try:
                published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                logger.warning(f"Invalid date format for publishedAt: {published_at}")
                published_at = None

        # Prepare the data for insertion
        processed_articles.append({
            'source_id': source_id,
            'source_name': source_name,
            'author': author,
            'title': title,
            'description': description,
            'url': url,
            'urlToImage': url_to_image,
            'publishedAt': published_at,
            'content': content
        })

    if not processed_articles:
        logger.error("No valid articles to insert.")
        return False

    return insert_data_into_db(processed_articles, 'newsapi')

def process_and_insert_gnews(api_response):
    pass

def process_and_insert_mediastack(api_response):
    pass

def process_and_insert_currentsapi(api_response):
    pass
