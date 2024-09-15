# scripts/apis/gnews_api.py

import os
from scripts.utils.helpers import fetch_news

def fetch_gnews(
    q,
    lang=None,
    country=None,
    max=10,
    in_param=None,
    nullable=None,
    from_param=None,
    to=None,
    sortby='publishedAt',
    page=1,
    expand=None
):
    """
    Fetch news from GNews API using the 'search' endpoint.

    Args:
        q (str): Keywords or phrases to search for. This parameter is mandatory.
            Supports logical operators. See query syntax in the documentation.
            Example: q='Apple AND iPhone'

        lang (str, optional): The 2-letter code of the language to filter articles.
            See the list of supported languages in the documentation.
            Example: lang='en'

        country (str, optional): The 2-letter code of the country where the news was published.
            See the list of supported countries in the documentation.
            Example: country='us'

        max (int, optional): The number of news articles to return. 
            Minimum is 1, maximum is 100. Default is 10.
            Example: max=50

        in_param (str, optional): Specifies which attributes to search for keywords.
            Possible values: 'title', 'description', 'content'.
            Can combine multiple attributes separated by commas.
            Example: in_param='title,description'

        nullable (str, optional): Specifies which attributes can have null values.
            Possible values: 'description', 'content', 'image'.
            Can combine multiple attributes separated by commas.
            Example: nullable='description,content'

        from_param (str, optional): Filter articles with a publication date greater than or equal to this value.
            Format: 'YYYY-MM-DDThh:mm:ssZ'
            Example: from_param='2024-09-15T00:00:00Z'

        to (str, optional): Filter articles with a publication date smaller than or equal to this value.
            Format: 'YYYY-MM-DDThh:mm:ssZ'
            Example: to='2024-09-15T23:59:59Z'

        sortby (str, optional): Specifies the sorting order of the articles.
            Possible values: 'publishedAt' (default), 'relevance'
            Example: sortby='relevance'

        page (int, optional): Controls the pagination of results. Default is 1.
            Only works with a paid subscription.
            Example: page=2

        expand (str, optional): Returns the full content of articles.
            Only works with a paid subscription.
            Set to 'content' to enable.
            Example: expand='content'

    Returns:
        dict: JSON response from the API.
    """
    url = "https://gnews.io/api/v4/search"
    params = {
        'token': os.getenv("GNEWS_API_KEY"),
        'q': q,
        'lang': lang,
        'country': country,
        'max': max,
        'in': in_param,
        'nullable': nullable,
        'from': from_param,
        'to': to,
        'sortby': sortby,
        'page': page,
        'expand': expand
    }
    params = {k: v for k, v in params.items() if v is not None}

    # Get the path of this script
    api_script_path = os.path.abspath(__file__)

    return fetch_news(url, params, 'gnews', api_script_path)