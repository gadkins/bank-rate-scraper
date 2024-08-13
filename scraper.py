import time
import random
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List, Dict, Optional, Tuple
import csv
import io
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from urllib.parse import urlparse


def fetch_tables(url: str, session: requests.Session, headers: Dict[str, str]) -> Tuple[str, Optional[List[Tag]]]:
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            return url, tables
        else:
            # Fall back to Selenium if requests fails
            # Useful if websites load content dynamically with JavaScript.
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(), options=chrome_options)

            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'table'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tables = soup.find_all('table')
            driver.quit()
            return url, tables
    except requests.RequestException as e:
        print(f"Failed to retrieve {url} with requests: {e}")
        return url, None
    except Exception as e:
        print(f"An error occurred with {url} using Selenium: {e}")
        return url, None

# Given a list of URLs, return a dictionary where each key is a URL and each value
# is a list of Tag objects representing the HTML table(s) for the given URL
def extract_all_tables_from_html(
    urls: List[str],
    max_workers: int = 10
) -> Tuple[Dict[str, Optional[List[Tag]]], List[Tuple[str, str]]]:
    """
    Given a list of URLs, return a dictionary where each key is a URL and each value
    is a list of Tag objects representing the HTML table(s) for the given URL, and
    a list of unsuccessful URLs with error messages.

    Args:
        urls (List[str]): List of URLs to process.
        max_workers (int): Maximum number of worker threads.

    Returns:
        Tuple[Dict[str, Optional[List[Tag]]], List[Tuple[str, str]]]:
        A dictionary with URLs as keys and lists of Tag objects as values, and
        a list of tuples containing unsuccessful URLs and their error messages.
    """
    result: Dict[str, Optional[List[Tag]]] = {}
    unsuccessful_urls: List[Tuple[str, str]] = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }

    session = requests.Session()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_tables, url, session, headers): url for url in urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                url, tables = future.result()
                result[url] = tables
            except Exception as e:
                print(f"An error occurred with {url}: {e}")
                result[url] = None
                unsuccessful_urls.append((url, str(e)))

    return result, unsuccessful_urls

def get_domain_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

def table_to_csv(table: Tag, domain: str) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    first_row = True
    for row in table.find_all('tr'):
        cols = row.find_all(['td', 'th'])
        row_data = [col.get_text(strip=True) for col in cols]
        if first_row:
            row_data.insert(0, domain)
            first_row = False
        writer.writerow(row_data)

    return output.getvalue()

def convert_tables_to_csv(results: Dict[str, Optional[List[Tag]]]) -> Dict[str, List[str]]:
    csv_results: Dict[str, List[str]] = {}

    for url, tables in results.items():
        if tables is None:
            csv_results[url] = []
            continue

        domain = get_domain_from_url(url)
        csv_tables = []
        for table in tables:
            csv_content = table_to_csv(table, domain)
            csv_tables.append(csv_content)

        csv_results[url] = csv_tables

    return csv_results