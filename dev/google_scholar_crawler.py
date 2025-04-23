import requests
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_coauthor_profiles(scholar_url):
    """
    Takes a Google Scholar profile URL and lists the profile URLs of coauthors.

    Args:
        scholar_url (str): The URL of the Google Scholar profile.

    Returns:
        list: A list of coauthor profile URLs.
    """
    coauthor_urls = []

    try:
        response = requests.get(scholar_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find coauthor links
        coauthor_elements = soup.select('a[href*="scholar.google.com/citations?user="]')
        for element in coauthor_elements:
            coauthor_url = element['href']
            if not coauthor_url.startswith('http'):
                coauthor_url = f"https://scholar.google.com{coauthor_url}"
            coauthor_urls.append(coauthor_url)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

    return coauthor_urls

if __name__ == "__main__":
    # Example usage
    scholar_profile_url = input("Enter the Google Scholar profile URL: ")
    coauthors = get_coauthor_profiles(scholar_profile_url)

    print("Coauthor profile URLs:")
    for url in coauthors:
        print(url)