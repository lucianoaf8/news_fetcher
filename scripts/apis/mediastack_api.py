import os
from scripts.utils.helpers import fetch_news


def fetch_mediastack(keywords, countries=None, categories=None, languages=None,
                     sort=None, limit=None, offset=None, date=None):
    """
    Fetch news from MediaStack API.

    Args:
        keywords (str): Keywords or phrases to search for.
        countries (str, optional): Comma-separated list of country codes. Defaults to None.
        categories (str, optional): Comma-separated list of categories. Defaults to None.
        languages (str, optional): Comma-separated list of languages. Defaults to None.
        sort (str, optional): Sorting order. Defaults to None.
        limit (int, optional): Limit the number of results. Defaults to None.
        offset (int, optional): Offset for pagination. Defaults to None.
        date (str, optional): Date range in 'YYYY-MM-DD,YYYY-MM-DD' format. Defaults to None.

    Returns:
        dict: JSON response from the API.
    """
    url = "http://api.mediastack.com/v1/news"
    params = {
        'access_key': os.getenv("MEDIASTACK_API_KEY"),
        'keywords': keywords,
        'countries': countries,
        'categories': categories,
        'languages': languages,
        'sort': sort,
        'limit': limit,
        'offset': offset,
        'date': date
    }
    params = {k: v for k, v in params.items() if v is not None}
    return fetch_news(url, params, 'mediastack')
