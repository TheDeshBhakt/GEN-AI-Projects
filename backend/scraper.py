import requests
from bs4 import BeautifulSoup
import json
import os

# --- Configuration ---
# In a real application, these would be managed more dynamically
# For now, we'll use a hardcoded list.
# I will use google_search to find better URLs later.
URLS_TO_SCRAPE = [
    "https://en.wikipedia.org/wiki/Varanasi",
    "https://varanasi.nic.in/tourist-places/",
    "https://varanasismartcity.gov.in/",
]

# The directory to save the scraped data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "scraped_data.json")

# --- Core Scraping Logic ---

def fetch_html(url: str):
    """Fetches the HTML content of a given URL."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html: str, url: str):
    """Parses HTML to extract relevant text content."""
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # This is a very basic parser. A real implementation would need
    # more sophisticated logic to handle different site layouts.
    # We'll extract text from common tags like <p>, <h1>, <h2>, etc.
    texts = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        texts.append(tag.get_text(strip=True))

    return {
        "url": url,
        "content": "\n".join(texts)
    }

def scrape_sites():
    """
    Main function to orchestrate the scraping process.
    - Fetches content from a list of URLs.
    - Parses the content.
    - Saves the data to a JSON file.
    """
    print("Starting the scraping process...")

    all_data = []
    for url in URLS_TO_SCRAPE:
        print(f"Scraping {url}...")
        html = fetch_html(url)
        parsed_data = parse_html(html, url)
        if parsed_data:
            all_data.append(parsed_data)

    # --- Save the data ---
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"Scraping complete. Data saved to {OUTPUT_FILE}")
    return {"status": "success", "message": f"Data saved to {OUTPUT_FILE}", "data_count": len(all_data)}

# --- To run this scraper independently ---
# You can run this file directly to test the scraping logic.
if __name__ == "__main__":
    scrape_sites()
