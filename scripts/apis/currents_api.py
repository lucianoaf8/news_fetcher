import os
from scripts.utils.helpers import fetch_news


def fetch_currents(keywords, language=None, country=None,
                   start_date=None, end_date=None):
    """
    Fetch news from Currents API.

    Args:
        keywords (str): Keywords or phrases to search for.
        language (str, optional): Language code. Defaults to None.
        country (str, optional): Country code. Defaults to None.
        start_date (str, optional): Start date in 'YYYY-MM-DD' format. Defaults to None.
        end_date (str, optional): End date in 'YYYY-MM-DD' format. Defaults to None.

    Returns:
        dict: JSON response from the API.
    """
    url = "https://api.currentsapi.services/v1/search"
    params = {
        'apiKey': os.getenv("CURRENTS_API_KEY"),
        'keywords': keywords,
        'language': language,
        'country': country,
        'start_date': start_date,
        'end_date': end_date
    }
    params = {k: v for k, v in params.items() if v is not None}
    return fetch_news(url, params, 'currents')
