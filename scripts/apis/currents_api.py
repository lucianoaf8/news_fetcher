import os
from datetime import datetime, timedelta
from scripts.utils.helpers import fetch_news

def fetch_currents(keywords=None, language=None, country=None, start_date=None, end_date=None,
                   type=None, category=None, page_number=None, domain=None, domain_not=None,
                   page_size=None, limit=None):
    """
    Fetch news articles from the Currents API.

    Args:
        keywords (str, optional): Exact match of words to search for in the title or description.
            Example:
                'neuropsychology statistics and breakthroughs'

        language (str, optional): Language code. Supported codes can be found at '/v1/available/languages'.
            Example:
                'en' for English

        country (str, optional): Country code representing news from a region. Supported codes at '/v1/available/regions'.
            Example:
                'US' for United States

        start_date (str, optional): Search news after the given date. Must be in RFC 3339 format 'YYYY-MM-DDTHH:MM:SS±HH:MM'.
            Default: Current time in UTC+0
            Example:
                '2023-10-01T00:00:00+00:00'

        end_date (str, optional): Search news before the given date. Must be in RFC 3339 format 'YYYY-MM-DDTHH:MM:SS±HH:MM'.
            Default: Current time in UTC+0
            Example:
                '2023-10-31T23:59:59+00:00'

        type (int, optional): Content type filter.
            Valid values:
                - 1: News
                - 2: Article
                - 3: Discussion content
            Default: All types (1, 2, and 3)

        category (str, optional): News category. Supported values can be found at '/v1/available/categories'.
            Example:
                'science'

        page_number (int, optional): Page number to access older news from current search results.
            Valid values: Any integer larger than zero.
            Default: 1

        domain (str, optional): Filter results by website domain (without 'www' or 'blog' prefix).
            Example:
                'scientificamerican.com'

        domain_not (str, optional): Exclude a website domain from results to blacklist it.
            Example:
                'example.com'

        page_size (int, optional): Number of articles per page.
            Valid values: Any integer between 1 and 200.
            Default: 30

        limit (int, optional): Total number of articles returned in results.
            Valid values: Any integer between 1 and 200.
            Note: Set to a small number (around 30) if you have a complex query.
            Default: Returns all matched articles by default.

    Returns:
        dict: JSON response from the API.

    Limitations:
        - **API Key Required**: You must set your API key in the 'CURRENTS_API_KEY' environment variable.
        - **Date Format**: 'start_date' and 'end_date' must be in RFC 3339 format: 'YYYY-MM-DDTHH:MM:SS±HH:MM'.
        - **Type Values**: 'type' must be 1, 2, or 3.
        - **Page Size Limit**: 'page_size' must be between 1 and 200.
        - **Limit**: 'limit' must be between 1 and 200.
        - **Valid Parameters**: Ensure all parameter values are valid according to the API documentation to avoid errors.

    Examples:
        Fetch the latest science news in English from the US, excluding articles from 'example.com':
            fetch_currents(
                keywords='neuropsychology statistics and breakthroughs',
                language='en',
                country='US',
                category='science',
                start_date='2023-10-01T00:00:00+00:00',
                end_date='2023-10-31T23:59:59+00:00',
                type=1,
                page_number=1,
                domain_not='example.com',
                page_size=30,
                limit=50
            )

        Search for articles from 'scientificamerican.com' domain in the last 7 days:
            fetch_currents(
                domain='scientificamerican.com',
                start_date=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                end_date=datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
                page_size=30
            )

    """
    url = "https://api.currentsapi.services/v1/search"
    api_key = os.getenv("CURRENTS_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Set 'CURRENTS_API_KEY' environment variable.")

    if page_size is not None and not (1 <= page_size <= 200):
        raise ValueError("page_size must be between 1 and 200.")

    if limit is not None and not (1 <= limit <= 200):
        raise ValueError("limit must be between 1 and 200.")

    if type is not None and type not in [1, 2, 3]:
        raise ValueError("type must be 1 (news), 2 (article), or 3 (discussion content).")

    params = {
        'apiKey': api_key,
        'keywords': keywords,
        'language': language,
        'country': country,
        'start_date': start_date,
        'end_date': end_date,
        'type': type,
        'category': category,
        'page_number': page_number,
        'domain': domain,
        'domain_not': domain_not,
        'page_size': page_size,
        'limit': limit
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    # Get the path of this script
    api_script_path = os.path.abspath(__file__)

    return fetch_news(url, params, 'currents', api_script_path)
