# scripts/apis/newsapi_api.py

import os
from scripts.utils.helpers import fetch_news

def fetch_newsapi(
    q=None,
    searchIn=None,
    sources=None,
    domains=None,
    excludeDomains=None,
    from_param=None,
    to=None,
    language=None,
    sortBy=None,
    pageSize=None,
    page=None
):
    """
    Fetch news from the 'everything' endpoint of NewsAPI.org.

    Args:
        q (str, optional): Keywords or phrases to search for in the article title and body.
            Advanced search is supported. Max length: 500 chars.
            Example: q='bitcoin AND (ethereum OR litecoin) NOT ripple'

        searchIn (str, optional): The fields to restrict your 'q' search to.
            Possible options: 'title', 'description', 'content'.
            Multiple options can be specified by separating them with a comma.
            Example: searchIn='title,content'

        sources (str, optional): A comma-separated string of identifiers for news sources or blogs.
            Example: sources='bbc-news,techcrunch,engadget'

        domains (str, optional): A comma-separated string of domains to restrict the search to.
            Example: domains='bbc.co.uk,techcrunch.com,engadget.com'

        excludeDomains (str, optional): A comma-separated string of domains to remove from the results.
            Example: excludeDomains='bbc.co.uk,techcrunch.com'

        from_param (str, optional): A date and optional time for the oldest article allowed.
            This should be in ISO 8601 format.
            Example: from_param='2024-09-15' or '2024-09-15T18:06:07'

        to (str, optional): A date and optional time for the newest article allowed.
            This should be in ISO 8601 format.
            Example: to='2024-09-15' or '2024-09-15T18:06:07'

        language (str, optional): The 2-letter ISO-639-1 code of the language to get headlines for.
            Possible options: 'ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'sv', 'ud', 'zh'
            Example: language='en'

        sortBy (str, optional): The order to sort the articles in.
            Possible options: 'relevancy', 'popularity', 'publishedAt'.
            Default: 'publishedAt'
            Example: sortBy='relevancy'

        pageSize (int, optional): The number of results to return per page (request).
            Default: 100. Maximum: 100.
            Example: pageSize=50

        page (int, optional): The page number to return.
            Use this to page through the results.
            Default: 1
            Example: page=2

    Returns:
        dict: JSON response from the API.
    """
    base_url = "https://newsapi.org/v2/everything"
    
    params = {
        'apiKey': os.getenv("NEWSAPI_KEY"),
        'q': q,
        'searchIn': searchIn,
        'sources': sources,
        'domains': domains,
        'excludeDomains': excludeDomains,
        'from': from_param,
        'to': to,
        'language': language,
        'sortBy': sortBy,
        'pageSize': pageSize,
        'page': page
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    # Get the path of this script
    api_script_path = os.path.abspath(__file__)

    return fetch_news(base_url, params, 'newsapi', api_script_path)