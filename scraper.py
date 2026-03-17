import requests
from bs4 import BeautifulSoup
import time

# Curated list of gardening sites known to have zone-specific content
TARGET_SITES = [
    "https://www.almanac.com",
    "https://extension.nmsu.edu",       # NM State University Extension - highly relevant
    "https://www.highcountrygardens.com", # NM-based native plant nursery
    "https://www.gardeningknowhow.com",
    "https://www.planetnatural.com",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_site_for_zone(site, zone, plant_name):
    """
    Builds a search URL using DuckDuckGo site: search to find relevant pages
    on a target site for a given zone and plant.
    Returns a list of URLs found.
    """
    site_host = site.replace("https://", "").replace("http://", "")
    query = f"{plant_name} zone {zone} {site_host}"

    try:
        response = requests.post(
            "https://lite.duckduckgo.com/lite/",
            data={"q": query},
            headers=HEADERS,
            timeout=10,
        )
        soup = BeautifulSoup(response.text, "html.parser")

        urls = []
        for a_tag in soup.find_all("a", class_="result-link", href=True):
            href = a_tag["href"]
            if site_host in href:
                urls.append(href)

        return urls[:3]  # Return top 3 results per site

    except Exception as e:
        print(f"  Search failed for {site}: {e}")
        return []

def scrape_page_for_tips(url, plant_name):
    """
    Fetches a page and extracts paragraphs likely to contain
    gardening tips relevant to the plant name.
    Returns a list of tip strings.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove nav, footer, script, style clutter
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        tips = []
        # Match on any keyword from the plant name (e.g. "Green Chile Pepper" -> ["green", "chile", "pepper"])
        keywords = [w for w in plant_name.lower().split() if len(w) > 3]

        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            text_lower = text.lower()
            if (
                any(kw in text_lower for kw in keywords)
                and len(text) > 80
                and len(text) < 1000
            ):
                tips.append(text)

        return tips[:5]  # Cap at 5 tips per page

    except Exception as e:
        print(f"  Could not scrape {url}: {e}")
        return []

def scrape_tips_for_plant(plant_name, zone):
    """
    Main scraping function for a single plant.
    Searches all target sites and aggregates tips.
    Returns a dict with source URLs and their tips.
    """
    print(f"  Scraping tips for: {plant_name}...")
    all_results = {}

    for site in TARGET_SITES:
        urls = search_site_for_zone(site, zone, plant_name)
        for url in urls:
            tips = scrape_page_for_tips(url, plant_name)
            if tips:
                all_results[url] = tips
        time.sleep(1)  # Be polite - don't hammer servers

    return all_results

def scrape_all_plants(plant_list, zone):
    """
    Runs scraping for every plant in the list.
    Returns a nested dict: {plant_name: {url: [tips]}}
    """
    results = {}
    for plant in plant_list:
        name = plant["name"]
        results[name] = scrape_tips_for_plant(name, zone)
        time.sleep(2)  # Pause between plants

    return results
