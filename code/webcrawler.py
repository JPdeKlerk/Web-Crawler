import requests
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from multiprocessing import Pool

def fetch_parse(url):
    """
    Fetches the HTML content of a webpage and parses links.

    Args:
    - url (str): The URL of the website.

    Returns:
    - content (str): The HTML content of the webpage.
    - links (list): A list of URLs found on the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [link['href'] for link in soup.find_all('a', href=True)]
        return response.content, links
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None, []

def process_url(url):
    """
    Process a single URL: fetches the content and saves it to a file.

    Args:
    - url (str): The URL to process.

    Returns:
    - links (list): A list of URLs found on the webpage.
    """
    response_content, links = fetch_parse(url)
    if response_content is not None:
        parsed_url = urlparse(url)
        url_name = parsed_url.netloc.split('.')[1]
        filename = f"{url_name}_{parsed_url.path.replace('/', '_')}"
        with open(os.path.join("files", filename), 'wb') as f:
            f.write(response_content)
        print(f"Successfully saved {filename}")
        return links
    return []

def crawl_website(start_url, num_processes=5, max_pages=100):
    """
    Web crawler that crawls HTML content with a breadth-first approach.

    Args:
    - start_url (str): The URL of the website.
    - num_processes (int): Number of parallel processes for crawling.
    - max_pages (int): Maximum number of pages to crawl.
    """
    visited_urls = set()
    urls_to_visit = [start_url]
    pages_count = 0

    with Pool(processes=num_processes) as pool:
        while urls_to_visit and pages_count < max_pages:
            current_url = urls_to_visit.pop(0)
            if current_url in visited_urls:
                continue
            links = pool.map(process_url, [current_url])[0]
            visited_urls.add(current_url)
            for link in links:
                if link.startswith(start_url) and link not in visited_urls and link not in urls_to_visit:
                    urls_to_visit.append(link)
            pages_count += 1
    print("Crawling finished.")

crawl_website("https://www.news24.com/", num_processes=50)
