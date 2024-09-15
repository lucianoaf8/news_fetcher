# scripts\apis\newsdata_api.py

"""
# Rate Limit Documentation for Newsdata.io API

The Newsdata.io API has a rate limit, which defines the number of requests that can be made to the API within a given time period. This rate limit helps to ensure that the API remains available to all users and prevents any one user from overloading the system.

Rate Limit by Plan:
- **Free Plan**: Allows 30 credits every 15 minutes.
- **Paid Plans**: Allow 1800 credits every 15 minutes.

If the rate limit is exceeded, the API will return a "Rate Limit Exceeded" error. Further requests will be blocked until the rate limit resets after 15 minutes.

For more details, refer to the official documentation on the rate limit of Newsdata.io.

# API Credit Limit for Different Plans - Newsdata.io

Newsdata.io API has a credit limit based on different subscription plans. This credit limit controls the amount of API usage available to users.

**Credit Limit by Plan:**
- **Free Plan**: 200 API credits per day, with a maximum of 10 results per API credit.
- **Basic Plan**: 20,000 API credits per month, with a maximum of 50 results per API credit.
- **Professional Plan**: 50,000 API credits per month, with a maximum of 50 results per API credit.
- **Corporate Plan**: 300,000 API credits per month, with a maximum of 50 results per API credit.

You can customize the number of articles per request from 1 to 50. For free users, the size must be between 1 and 10.

**Example:**
For a paid user, the following request retrieves 15 articles per page/request:
```
https://newsdata.io/api/1/latest?apikey=pub_530693ab6200c74e7e6f62b4c741aa9d07bc4&q=YOUR_QUERY&size=15
```

For free users, the size parameter must be set between 1 and 10.

Please refer to the official documentation for more details on API credit limits for each subscription plan.

# Categories - Newsdata.io

The Newsdata.io API provides access to various categories of news. Below are the available categories:

- business
- crime
- domestic
- education
- entertainment
- environment
- food
- health
- lifestyle
- other
- politics
- science
- sports
- technology
- top
- tourism
- world

You can use these categories to filter news based on your interests.

"""

import os
from scripts.utils.helpers import fetch_news
from scripts.utils.process_fetched_data import process_and_insert_data

def fetch_newsdata(
    endpoint,
    id=None,
    q=None,
    qInTitle=None,
    qInMeta=None,
    timeframe=None,
    from_date=None,
    to_date=None,
    country=None,
    category=None,
    excludecategory=None,
    language=None,
    tag=None,
    sentiment=None,
    region=None,
    domain=None,
    domainurl=None,
    excludedomain=None,
    excludefield=None,
    prioritydomain=None,
    timezone=None,
    full_content=None,
    image=None,
    video=None,
    removeduplicate=None,
    size=None,
    page=None
):
    """
    Fetch news from NewsData.io API.

    Args:
        endpoint (str): Required. The API endpoint to use ('latest' or 'archive').

        id (str, optional): Search for specific news articles using their unique "article_id" strings.
            You can add up to 50 article IDs in a single query.
            Example: id='article_id1,article_id2'

        q (str, optional): Search news articles for specific keywords or phrases present in the news
            title, content, URL, meta keywords, and meta description.
            The value must be URL-encoded and the maximum character limit is 512 characters.
            Example: q='pizza'

        qInTitle (str, optional): Search news articles for specific keywords or phrases present in the news titles only.
            Cannot be used with 'q' or 'qInMeta' in the same query.
            Example: qInTitle='pizza'

        qInMeta (str, optional): Search news articles for specific keywords or phrases present in the news titles,
            URL, meta keywords, and meta description only.
            Cannot be used with 'q' or 'qInTitle' in the same query.
            Example: qInMeta='pizza'

        timeframe (str, optional): (Only for 'latest' endpoint)
            Search the news articles for a specific timeframe in hours or minutes.
            For hours: 1 to 48 (e.g., '6' for 6 hours)
            For minutes: 1m to 2880m (e.g., '15m' for 15 minutes)
            Example: timeframe='6' or timeframe='15m'

        from_date (str, optional): (Only for 'archive' endpoint)
            Fetch news data from a particular date in the past.
            Format: 'YYYY-MM-DD'
            Example: from_date='2021-12-26'

        to_date (str, optional): (Only for 'archive' endpoint)
            Set an end date for the search result.
            Format: 'YYYY-MM-DD'
            Example: to_date='2024-09-13'

        country (str, optional): Search the news articles from specific countries.
            You can add up to 5 country codes in a single query.
            Example: country='au,us'

        category (str, optional): Search the news articles for specific categories.
            You can add up to 5 categories in a single query.
            Example: category='sports,technology'

        excludecategory (str, optional): Exclude specific categories from the search.
            Cannot be used simultaneously with 'category'.
            Example: excludecategory='top'

        language (str, optional): Search the news articles for specific languages.
            You can add up to 5 language codes in a single query.
            Example: language='en,fr'

        tag (str, optional): (Available only for Professional and Corporate users)
            Search the news articles for specific AI-classified tags.
            You can add up to 5 tags in a single query.
            Example: tag='food,tourism'

        sentiment (str, optional): (Available only for Professional and Corporate users)
            Search the news articles based on the sentiment (positive, negative, neutral).
            Example: sentiment='positive'

        region (str, optional): (Available only for Corporate users)
            Search the news articles for specific geographical regions.
            You can add up to 5 regions in a single query.
            Example: region='new york,chicago'

        domain (str, optional): Search the news articles from specific domains or news sources.
            You can add up to 5 domains in a single query.
            Example: domain='nytimes,bbc'

        domainurl (str, optional): Search the news articles from specific domains using their URLs.
            You can add up to 5 domain URLs in a single query.
            Example: domainurl='nytimes.com,bbc.co.uk'

        excludedomain (str, optional): Exclude specific domains or news sources from the search.
            You can exclude up to 5 domains in a single query.
            Example: excludedomain='cnn.com,foxnews.com'

        excludefield (str, optional): Exclude specific response fields from the API response.
            Cannot exclude 'article_id'.
            Example: excludefield='pubDate,source_icon'

        prioritydomain (str, optional): Search the news articles only from top news domains.
            Options:
                'top' - Top 10% of news domains
                'medium' - Top 30% of news domains
                'low' - Top 50% of news domains
            Example: prioritydomain='top'

        timezone (str, optional): Search the news articles for a specific timezone.
            Example: timezone='America/New_York'

        full_content (int, optional): Search for news articles with full content or without full content.
            Use '1' for articles with full content and '0' for without.
            Example: full_content=1

        image (int, optional): Search for news articles with or without featured images.
            Use '1' for articles with images and '0' for without.
            Example: image=1

        video (int, optional): Search for news articles with or without videos.
            Use '1' for articles with videos and '0' for without.
            Example: video=0

        removeduplicate (int, optional): (Only for 'latest' endpoint)
            Use '1' to remove duplicate articles.
            Example: removeduplicate=1

        size (int, optional): Customize the number of articles per API request.
            Range: 1 to 50 (Free user max: 10, Paid user max: 50)
            Example: size=25

        page (str, optional): Use to navigate to the next page in paginated results.
            Example: page='XXXPPPXXXXXXXXXX'

    Returns:
        dict: JSON response from the API.

    Raises:
        ValueError: If invalid parameters are provided.
    """
    if endpoint not in ['latest', 'archive']:
        raise ValueError("Invalid endpoint. Choose 'latest' or 'archive'.")

    # Validate exclusive parameters
    if sum(bool(param) for param in [q, qInTitle, qInMeta]) > 1:
        raise ValueError("You can use only one of 'q', 'qInTitle', or 'qInMeta' in the same query.")

    if category and excludecategory:
        raise ValueError("You cannot use 'category' and 'excludecategory' simultaneously.")

    if endpoint == 'latest':
        if from_date or to_date:
            raise ValueError("'from_date' and 'to_date' are only valid for the 'archive' endpoint.")
    elif endpoint == 'archive':
        if timeframe or removeduplicate:
            raise ValueError("'timeframe' and 'removeduplicate' are only valid for the 'latest' endpoint.")
        # Ensure at least one required parameter is provided for 'archive'
        if not any([q, qInTitle, qInMeta, domain, country, category, language, full_content, image, video, prioritydomain, domainurl]):
            raise ValueError("For 'archive' endpoint, at least one of ['q','qInTitle','qInMeta','domain','country','category','language','full_content','image','video','prioritydomain','domainurl'] must be provided.")

    # Handle category parameter
    if isinstance(category, list):
        category = ','.join(filter(None, category))  # Join non-empty strings
    elif isinstance(category, str):
        category = category.strip()  # Remove any leading/trailing whitespace

    url = f"https://newsdata.io/api/1/{endpoint}"
    params = {
        'apikey': os.getenv("NEWSDATA_API_KEY"),
        'id': id,
        'q': q,
        'qInTitle': qInTitle,
        'qInMeta': qInMeta,
        'timeframe': timeframe if endpoint == 'latest' else None,
        'from_date': from_date if endpoint == 'archive' else None,
        'to_date': to_date if endpoint == 'archive' else None,
        'country': country,
        'category': category,
        'excludecategory': excludecategory,
        'language': language,
        'tag': tag,
        'sentiment': sentiment,
        'region': region,
        'domain': domain,
        'domainurl': domainurl,
        'excludedomain': excludedomain,
        'excludefield': excludefield,
        'prioritydomain': prioritydomain,
        'timezone': timezone,
        'full_content': full_content,
        'image': image,
        'video': video,
        'removeduplicate': removeduplicate if endpoint == 'latest' else None,
        'size': size,
        'page': page,
    }
    # Remove parameters that are None or empty strings
    params = {k: v for k, v in params.items() if v not in [None, '']}


    # Get the path of this script
    api_script_path = os.path.abspath(__file__)

    # Fetch the news data
    return fetch_news(url, params, 'newsdata', api_script_path)