# Project Documentation: News Fetcher

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Code Organization](#code-organization)
   - [Main Script](#main-script)
   - [API Modules](#api-modules)
   - [Utility Modules](#utility-modules)
7. [Extending the Project](#extending-the-project)
8. [Logging and Error Handling](#logging-and-error-handling)
9. [Data Storage](#data-storage)
10. [Dependencies](#dependencies)
11. [FAQs](#faqs)
12. [Contributing](#contributing)

---

## Introduction

The **News Fetcher** project is a Python application designed to fetch news articles from multiple news APIs, including:

- **NewsData.io**
- **NewsAPI.org**
- **GNews**
- **MediaStack**
- **Currents API**

The application is modular, adhering to best practices in Python programming and software design. It follows PEP 8 style guidelines for readability and maintainability.

---

## Project Structure

```
NEWS_FETCHER/
├── fetched_news/
├── logs/
│   ├── api_base.log
│   ├── data_saver.log
│   ├── helpers.log
│   ├── news_api.log
├── scripts/
│   ├── apis/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── currents_api.py
│   │   ├── gnews_api.py
│   │   ├── mediastack_api.py
│   │   ├── newsapi_api.py
│   │   ├── newsdata_api.py
│   ├── utils/
│       ├── __pycache__/
│       ├── helpers.py
│       ├── logger_config.py
├── .env
├── main.py
```

- **`fetched_news/`**: Directory where fetched news data is stored, grouped by timestamp.
- **`logs/`**: Contains log files for different modules.
- **`scripts/`**: Contains API modules and utility modules.
- **`main.py`**: The main script to run the application.
- **`.env`**: Environment variables file for API keys.

---

## Installation

### Prerequisites

- **Python 3.6+** installed on your system.

### Steps

1. **Clone or Download the Project**

   Download the project files and navigate to the `NEWS_FETCHER` directory.

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

### Setting Up API Keys

The project requires API keys to access the different news APIs. You need to sign up for each API service and obtain an API key.

1. **Create a `.env` File**

   In the project root directory (`NEWS_FETCHER/`), create a `.env` file.

   ```bash
   touch .env
   ```

2. **Add Your API Keys**

   Open the `.env` file and add your API keys:

   ```env
   NEWSDATA_API_KEY=your_newsdata_api_key
   NEWSAPI_KEY=your_newsapi_key
   GNEWS_API_KEY=your_gnews_api_key
   MEDIASTACK_API_KEY=your_mediastack_api_key
   CURRENTS_API_KEY=your_currents_api_key
   ```

   Replace `your_api_key` with the actual API keys you obtained.

### Directory Permissions

Ensure that the `fetched_news/` and `logs/` directories have the necessary permissions for the application to write data.

---

## Usage

### Running the Application

Navigate to the `NEWS_FETCHER/` directory and run the `main.py` script:

```bash
cd NEWS_FETCHER
python main.py
```

### Example Output

The application will fetch news data from the specified APIs and save the results in JSON format under the `fetched_news/` directory, grouped by a timestamped folder.

### Customizing API Calls

You can customize which APIs to fetch data from and provide specific parameters for each API. Modify the `main()` function call in `main.py`:

```python
if __name__ == "__main__":
    result = main(
        apis_to_fetch=['newsdata', 'newsapi'],
        newsdata={
            'q': 'technology',
            'country': 'us',
            'from_date': '2023-01-01',
            'to_date': '2023-01-31'
        },
        newsapi={
            'q': 'python programming',
            'language': 'en',
            'from_date': '2023-01-01',
            'to_date': '2023-01-31'
        }
    )
    print(json.dumps(result, indent=2))
```

---

## Code Organization

### Main Script

**`main.py`**

- Serves as the entry point of the application.
- Contains the `main()` function, which orchestrates fetching and saving news data.
- Uses the `run_apis()` function to call API-specific functions based on user input.

### API Modules

Each API has its own module under `scripts/apis/`:

- **`newsdata_api.py`**
- **`newsapi_api.py`**
- **`gnews_api.py`**
- **`mediastack_api.py`**
- **`currents_api.py`**

Each module contains a `fetch_<api_name>()` function that:

- Constructs the API request URL and parameters.
- Calls the generic `fetch_news()` function from `helpers.py`.

### Utility Modules

**`scripts/utils/helpers.py`**

- Contains the `fetch_news()` function, which handles HTTP requests, retries, and error handling.
- Includes the `save_news_data()` function to save fetched data.

**`scripts/utils/logger_config.py`**

- Configures and returns a logger object for consistent logging across modules.

---

## Extending the Project

### Adding a New API

1. **Create a New Module**

   Create a new Python file in `scripts/apis/`, e.g., `new_api.py`.

2. **Implement the Fetch Function**

   ```python
   import os
   from scripts.utils.helpers import fetch_news

   def fetch_new_api(param1, param2):
       """
       Fetch news from New API.

       Args:
           param1 (type): Description.
           param2 (type): Description.

       Returns:
           dict: JSON response from the API.
       """
       url = "https://newapi.com/v1/data"
       params = {
           'api_key': os.getenv("NEW_API_KEY"),
           'param1': param1,
           'param2': param2
       }
       params = {k: v for k, v in params.items() if v is not None}
       return fetch_news(url, params, 'new_api')
   ```

3. **Update `__init__.py`**

   Add the import statement to `scripts/apis/__init__.py`:

   ```python
   from .new_api import fetch_new_api
   ```

4. **Add API Key to `.env`**

   ```env
   NEW_API_KEY=your_new_api_key
   ```

5. **Update `main.py`**

   Include the new API in the `api_functions` dictionary and use it in `main()`.

### Customizing Error Handling

Modify the `fetch_news()` function in `helpers.py` to adjust retry logic or error responses.

---

## Logging and Error Handling

- **Logging Levels:**

  - **DEBUG:** Detailed information for diagnosing problems.
  - **INFO:** Confirmation that things are working as expected.
  - **WARNING:** An indication of unexpected events.
  - **ERROR:** Serious problems that prevent function execution.

- **Log Files:**

  Logs are stored in the `logs/` directory:

  - `api_base.log`
  - `data_saver.log`
  - `helpers.log`
  - `news_api.log`

- **Error Handling:**

  - The `fetch_news()` function implements retries with exponential backoff.
  - Exceptions are caught and logged appropriately.
  - If the maximum number of retries is reached, the function logs an error and returns `None`.

---

## Data Storage

- **Directory Structure:**

  ```
  fetched_news/
  └── YYYYMMDD_HHMMSS/
      ├── newsdata_data.json
      ├── newsapi_data.json
      ├── gnews_data.json
      ├── mediastack_data.json
      └── currents_data.json
  ```

- **File Naming:**

  Each API's data is saved in a JSON file named `<api_name>_data.json`.

- **Data Grouping:**

  Data is grouped by timestamped folders within `fetched_news/`, based on when the data was fetched.

---

## Dependencies

Listed in `requirements.txt`:

- **requests**
- **python-dotenv**

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## FAQs

### 1. **I get an error saying an API key is missing.**

Ensure that you've added all the necessary API keys to your `.env` file.

### 2. **How can I fetch data from only one API?**

Modify the `apis_to_fetch` parameter in the `main()` function:

```python
result = main(
    apis_to_fetch=['newsapi'],
    newsapi={
        'q': 'climate change',
        'language': 'en'
    }
)
```

### 3. **Can I schedule this script to run periodically?**

Yes, you can use scheduling tools like `cron` on Unix systems or `Task Scheduler` on Windows to run the script at desired intervals.

### 4. **Where can I find the logs?**

Logs are stored in the `logs/` directory at the project root.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Create a Feature Branch**

   ```bash
   git checkout -b feature/new-feature
   ```

2. **Commit Changes**

   ```bash
   git commit -am 'Add new feature'
   ```

3. **Push to the Branch**

   ```bash
   git push origin feature/new-feature
   ```

4. **Notify the Project Maintainer**

   Since the project is in development and not hosted on GitHub, inform the project maintainer to review your changes.

---

**Thank you for using the News Fetcher! If you have any questions or need further assistance, feel free to reach out.**

---

## Updated Code Snippets

Below are the updated code snippets reflecting the latest project structure and changes.

### `main.py`

```python
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the project root to the Python path
import sys
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from scripts.utils.logger_config import get_logger
from scripts.utils.helpers import save_news_data, run_apis

# Initialize logger
logger = get_logger('news_api')

# Load environment variables
load_dotenv()


def main(apis_to_fetch=None, **kwargs):
    """
    Main function to orchestrate fetching and saving news data.

    Args:
        apis_to_fetch (list, optional): List of APIs to fetch. Defaults to all APIs.
        **kwargs: Additional keyword arguments for API parameters.

    Returns:
        dict: A dictionary containing news data from each API.
    """
    try:
        if apis_to_fetch is None:
            apis_to_fetch = ['newsdata', 'newsapi', 'gnews', 'mediastack', 'currents']
        elif isinstance(apis_to_fetch, str):
            apis_to_fetch = [apis_to_fetch]

        news_data = run_apis(apis_to_fetch, **kwargs)
        save_news_data(news_data)
        logger.info("News data fetched and saved successfully")
        return news_data
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")
        return None


if __name__ == "__main__":
    # Example usage
    result = main(
        apis_to_fetch=[
            'newsdata',
            'newsapi',
            'gnews',
            'mediastack',
            'currents'
        ],
        newsdata={
            'q': 'elections',
            'country': 'us',
            'from_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        },
        newsapi={
            'q': 'volleyball',
            'sort_by': 'publishedAt',
            'page_size': 10,
            'from_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        },
        gnews={
            'q': 'triathlon tips',
            'max': 5,
            'from_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'to': datetime.now().strftime('%Y-%m-%d')
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
```

### `scripts/utils/helpers.py`

```python
import os
import time
import json
import requests
from datetime import datetime
from scripts.utils.logger_config import get_logger

# Initialize logger
logger = get_logger('helpers')

# Add the project root to the Python path
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.apis import (
    fetch_newsdata,
    fetch_newsapi,
    fetch_gnews,
    fetch_mediastack,
    fetch_currents
)


def fetch_news(url, params, api_name, max_retries=3):
    """
    Fetch news data from a given API.

    Args:
        url (str): API endpoint URL.
        params (dict): Parameters for the API call.
        api_name (str): Name of the API.
        max_retries (int, optional): Maximum number of retries. Defaults to 3.

    Returns:
        dict or None: JSON response from the API or None if failed.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            logger.info(f"Successfully fetched data from {api_name}")
            return data
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt + 1} failed for {api_name}: {str(e)}")
            logger.error(f"Request URL: {response.url}")
            if attempt == max_retries - 1:
                logger.error(f"Max retries reached for {api_name}. Giving up.")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff


def save_news_data(news_data):
    """
    Save the fetched news data to JSON files.

    Args:
        news_data (dict): Dictionary containing news data from each API.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_path = os.path.join(project_root, 'fetched_news', timestamp)
    os.makedirs(folder_path, exist_ok=True)

    for api_name, api_data in news_data.items():
        filename = f'{api_name}_data.json'
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'w') as f:
            json.dump(api_data, f, indent=4)

        logger.info(f"{api_name} data saved to {file_path}")


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
            news_data[api] = api_functions[api](**api_params)
        else:
            logger.warning(f"Skipping unknown API: {api}")

    return news_data
```

### `scripts/apis/__init__.py`

```python
from .newsdata_api import fetch_newsdata
from .newsapi_api import fetch_newsapi
from .gnews_api import fetch_gnews
from .mediastack_api import fetch_mediastack
from .currents_api import fetch_currents
```

---

**Note:** The code snippets provided above reflect the updated project structure and the changes requested. The paths and imports have been adjusted to match the new folder organization.

---

**Thank you for your interest in the News Fetcher project! If you have any questions or need further assistance, please feel free to reach out.**