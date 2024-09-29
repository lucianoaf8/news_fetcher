import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the project root to the Python path
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from scripts.utils.logger_config import get_logger
from scripts.utils.helpers import save_news_data
from scripts.utils.get_interests import get_interests
from scripts.apis import (
    fetch_newsdata,
    fetch_newsapi,
    fetch_gnews,
    fetch_mediastack,
    fetch_currents
)

# Initialize logger
logger = get_logger('main')

# Load environment variables
load_dotenv()

def run_apis(apis_to_fetch, **kwargs):
    """
    Run the specified APIs and collect the news data.

    Args:
        apis_to_fetch (list): List of API names to fetch data from.
        **kwargs: Additional keyword arguments for API parameters.

    Returns:
        dict: A dictionary containing news data from each API.
    """
    news_data = {}
    api_functions = {
        'newsdata': fetch_newsdata,
        'newsapi': fetch_newsapi,
        'gnews': fetch_gnews,
        'mediastack': fetch_mediastack,
        'currents': fetch_currents
    }

    for api in apis_to_fetch:
        if api in api_functions:
            api_params = kwargs.get(api, {})
            # Ensure all parameters are JSON serializable
            api_params = {k: (list(v) if isinstance(v, set) else v) for k, v in api_params.items()}
            try:
                logger.debug(f"Fetching data from API: {api} with params: {api_params}")
                news_data[api] = api_functions[api](**api_params)
                logger.debug(f"Successfully fetched data from API: {api}")
            except Exception as api_e:
                logger.error(f"Error fetching data from API {api}: {str(api_e)}")
                news_data[api] = None
        else:
            logger.warning(f"Skipping unknown API: {api}")

    return news_data

def fetch_news_for_interest(apis_to_fetch, interest):
    """
    Fetch news for a single interest from NewsData, NewsAPI, and GNews.

    Args:
        interest (dict): A dictionary containing interest data.

    Returns:
        dict: A dictionary containing news data from NewsData, NewsAPI, and GNews for the interest.
    """
    
    common_params = {
        'q': interest['formatted_interest'],
        'language': interest['language']
    }

    kwargs = {
        'newsdata': {
            'endpoint': 'latest',
            'category': interest['category'],
            'country': interest['country'],
            **common_params
        },
        'newsapi': {
            'searchIn': 'title,description',
            'from_param': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d'),
            **common_params
        },
        'gnews': {
            'max': 10,  # You can adjust this or make it dynamic based on requirements
            'from_param': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'to': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'in_param': 'title,description',
            'nullable': 'image',
            'lang': interest['language'],
            'q': interest['formatted_interest']
        }
    }

    return run_apis(apis_to_fetch, **kwargs)


def main(fetch_interests_flag=False, apis_to_fetch=None, **kwargs):
    """
    Main function to orchestrate fetching and saving news data.

    Args:
        fetch_interests_flag (bool): If True, fetch news for interests from the database.
        apis_to_fetch (list, optional): List of APIs to fetch. Defaults to all APIs.
        **kwargs: Additional keyword arguments for API parameters.

    Returns:
        dict: A dictionary containing news data from each API.
    """
    try:
        if fetch_interests_flag:
            interests = get_interests()
            logger.debug(f"Retrieved {len(interests)} interests from the database.")

            # Initialize news_data with APIs as keys
            news_data = { api: {} for api in apis_to_fetch }

            for interest in interests:
                logger.info(f"Fetching news for interest: {interest['formatted_interest']} (ID: {interest['id']})")
                interest_news = fetch_news_for_interest(apis_to_fetch, interest)
                for api, data in interest_news.items():
                    if data is not None:
                        news_data[api][interest['id']] = data
                        logger.info(f"Added data for API '{api}' and interest ID '{interest['id']}'.")
                    else:
                        logger.warning(f"No data returned for API '{api}' and interest ID '{interest['id']}'.")

            logger.info("Completed fetching news for all interests.")
        else:
            if apis_to_fetch is not None:
                if isinstance(apis_to_fetch, str):
                    apis_to_fetch = [apis_to_fetch]
            else:
                # If no APIs specified, fetch from all available APIs
                apis_to_fetch = ['newsdata', 'newsapi', 'gnews', 'mediastack', 'currents']

            # Ensure all parameters are JSON serializable
            for api, params in kwargs.items():
                kwargs[api] = {k: (list(v) if isinstance(v, set) else v) for k, v in params.items()}

            logger.debug(f"Fetching news from APIs: {apis_to_fetch} with parameters: {kwargs}")
            news_data = run_apis(apis_to_fetch, **kwargs)
            logger.info("Completed fetching news from specified APIs.")

        # Save the collected news data
        save_news_data(news_data)
        logger.info("News data fetched and saved successfully.")
        return news_data
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    # To fetch news for interests from the database:
    # result = main(fetch_interests_flag=True)

    # To test with custom parameters:
    result = main(
        fetch_interests_flag=False,
        apis_to_fetch=[
            # 'newsdata',
            # 'newsapi',
            # 'gnews',
            # 'mediastack',
            'currents'
        ],
        newsdata={
            'endpoint': 'latest',
            'q': 'pop culture',
            'country': 'ca',
            'language': 'en',
            'category': [
                # 'business',
                # 'crime',
                # 'domestic',
                # 'education',
                # 'entertainment',
                # 'environment',
                # 'food',
                # 'health',
                # 'lifestyle',
                # 'other',
                # 'politics',
                # 'science',
                # 'sports',
                # 'technology',
                # 'top',
                # 'tourism',
                # 'world'
            ]
        },
        newsapi={
            'q': 'prompt engineering',
            'searchIn': 'title,description',
            'from_param': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d'),
            'language': 'en',
        },
        gnews={
            'q': 'cultura pop brasil',
            'max': 10,
            'lang': 'pt',
            'from_param': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'to': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'in_param': 'title,description',
            'nullable': 'image'
        },
        mediastack={
            'limit': 30,
            'keywords': 'machine learning',

            'categories': 'technology, -general, -science',
            # general - Uncategorized News
            # business - Business News
            # entertainment - Entertainment News
            # health - Health News
            # science - Science News
            # sports - Sports News
            # technology - Technology News

            'countries': 'us',
            'languages': 'en',
            # 'date': f"{(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')},{datetime.now().strftime('%Y-%m-%d')}",
            'sort': 'popularity',
        },
        currents={
                'keywords': 'Fofoca de artista',
                'language': 'pt',
                'country': 'BR',
                
                'category': 'regional',
                #    "regional",
                #     "technology",
                #     "lifestyle",
                #     "business",
                #     "general",
                #     "programming",
                #     "science",
                #     "entertainment",
                #     "world",
                #     "sports",
                #     "finance",
                #     "academia",
                #     "politics",
                #     "health",
                #     "opinion",
                #     "food",
                
                'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                'end_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                'type': 1,
                'page_number': 1,
                # 'domain': 'scientificamerican.com',
                # 'domain_not': 'example.com',
                'page_size': 30,
                # 'limit': 50
        }
    )
    logger.debug((json.dumps(result, indent=2)))
