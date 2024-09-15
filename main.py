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
logger = get_logger('news_api')

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
            news_data[api] = api_functions[api](**api_params)
        else:
            logger.warning(f"Skipping unknown API: {api}")

    return news_data

def fetch_news_for_interest(interest):
    """
    Fetch news for a single interest from NewsData and NewsAPI.

    Args:
        interest (dict): A dictionary containing interest data.

    Returns:
        dict: A dictionary containing news data from NewsData and NewsAPI for the interest.
    """
    apis_to_fetch = ['newsdata', 'newsapi']
    common_params = {
        'q': interest['formatted_interest'],
        'language': interest['language'],
        'country': interest['country'],
    }

    kwargs = {
        'newsdata': {
            'endpoint': 'latest',
            'category': interest['category'],
            **common_params
        },
        'newsapi': {
            'searchIn': 'title,description',
            'from_param': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d'),
            **common_params
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
            all_news_data = {}
            for interest in interests:
                logger.info(f"Fetching news for interest: {interest['formatted_interest']}")
                interest_news = fetch_news_for_interest(interest)
                all_news_data[interest['id']] = interest_news
            news_data = all_news_data
        else:
            if apis_to_fetch is None:
                apis_to_fetch = ['newsdata', 'newsapi', 'gnews', 'mediastack', 'currents']
            elif isinstance(apis_to_fetch, str):
                apis_to_fetch = [apis_to_fetch]

            # Ensure all parameters are JSON serializable
            for api, params in kwargs.items():
                kwargs[api] = {k: (list(v) if isinstance(v, set) else v) for k, v in params.items()}

            news_data = run_apis(apis_to_fetch, **kwargs)

        save_news_data(news_data)
        logger.info("News data fetched and saved successfully")
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
        apis_to_fetch=[
            # 'newsdata',
            # 'newsapi',
            'gnews',
            # 'mediastack',
            # 'currents'
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
            'q': 'triathlon',
            'max': 10,
            'lang': 'en',
            'from_param': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'to': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'in_param': 'title,description',
            'nullable': 'image'
        },
        mediastack={
            'keywords': 'travel on a budget',
            'countries': 'us,gb',
            'limit': 5,
            'date': f"{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')},{datetime.now().strftime('%Y-%m-%d')}"
        },
        currents={
            'keywords': 'neuropsychology statistics and breakthroughs',
            'start_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d')
        }
    )
    print(json.dumps(result, indent=2))