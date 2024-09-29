import os
from scripts.utils.helpers import fetch_news

def fetch_mediastack(keywords=None, sources=None, categories=None, countries=None, languages=None,
                     date=None, sort=None, limit=None, offset=None):
    """
    Fetch news articles from the Mediastack API.

    Args:
        keywords (str, optional): Search for sentences or keywords. You can exclude words by prepending them with a '-'.
            Examples:
                'new movies 2021' - Search for "new movies 2021".
                'new movies 2021, -matrix' - Search for "new movies 2021" but exclude "matrix".

        sources (str, optional): Include or exclude one or multiple comma-separated news sources. Exclude sources by prepending them with a '-'.
            Examples:
                'cnn' - Include only CNN.
                'cnn,-bbc' - Include CNN but exclude BBC.

        categories (str, optional): Include or exclude one or multiple comma-separated news categories. Exclude categories by prepending them with a '-'.
            Available categories:
                'general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology'.
            Examples:
                'health,-sports' - Include health news but exclude sports news.

        countries (str, optional): Include or exclude one or multiple comma-separated country codes. Exclude countries by prepending them with a '-'.
            Examples:
                'us,gb,de' - Include US, GB, and DE.
                'au,-us' - Include Australia but exclude US.

        languages (str, optional): Include or exclude one or multiple comma-separated language codes. Exclude languages by prepending them with a '-'.
            Available languages:
                'ar' - Arabic
                'de' - German
                'en' - English
                'es' - Spanish
                'fr' - French
                'he' - Hebrew
                'it' - Italian
                'nl' - Dutch
                'no' - Norwegian
                'pt' - Portuguese
                'ru' - Russian
                'se' - Swedish
                'zh' - Chinese
            Examples:
                'en,-de' - Include English but exclude German.

        date (str, optional): Specify a date or date range in 'YYYY-MM-DD' format. For a date range, separate start and end dates with a comma.
            Examples:
                '2020-01-01' - News on Jan 1st, 2020.
                '2020-12-24,2020-12-31' - News between Dec 24th and Dec 31st, 2020.

        sort (str, optional): Specify the sorting order. Available values:
            'published_desc' (default), 'published_asc', 'popularity'.

        limit (int, optional): Specify the number of results per page. Default is 25, maximum is 100.

        offset (int, optional): Specify the pagination offset value. Default is 0.

    Returns:
        dict: JSON response from the API.

    Limitations:
        - **Access Key Required**: You must set your API access key in the 'MEDIASTACK_API_KEY' environment variable.
        - **HTTPS Encryption**: Available only on the Standard Plan and higher. Free Plan users are limited to HTTP connections.
        - **Live News Delay**: Free Plan users receive news with a 30-minute delay. Upgrade to the Standard Plan or higher for real-time news.
        - **Maximum Limit**: The 'limit' parameter cannot exceed 100.
        - **Parameter Values**: Ensure that parameter values are valid as per the API documentation to avoid errors.

    Examples:
        Fetch the latest technology news in English, excluding articles from CNN:
            fetch_mediastack(categories='technology', languages='en', sources='-cnn')

        Search for news about 'artificial intelligence' published between two dates:
            fetch_mediastack(keywords='artificial intelligence', date='2021-01-01,2021-12-31')

    """
    url = "http://api.mediastack.com/v1/news"
    access_key = os.getenv("MEDIASTACK_API_KEY")
    if not access_key:
        raise ValueError("API access key not found. Set 'MEDIASTACK_API_KEY' environment variable.")

    if limit is not None and limit > 100:
        raise ValueError("Limit cannot exceed 100.")

    valid_sort_options = ['published_desc', 'published_asc', 'popularity']
    if sort is not None and sort not in valid_sort_options:
        raise ValueError(f"Invalid sort option. Choose from {valid_sort_options}.")

    params = {
        'access_key': access_key,
        'keywords': keywords,
        'sources': sources,
        'categories': categories,
        'countries': countries,
        'languages': languages,
        'date': date,
        'sort': sort,
        'limit': limit,
        'offset': offset
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    # Get the path of this script
    api_script_path = os.path.abspath(__file__)
    
    
    return fetch_news(url, params, 'mediastack', api_script_path)
