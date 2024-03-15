from bs4 import BeautifulSoup
import requests

NEWS_URL = "https://www.prothomalony.com/"

# Sample function to scrape Bangla news headlines and articles
def scrape_bangla_news():
    try:
        url = f"{NEWS_URL}"

        # Send GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract headlines and articles (you need to adjust this based on the website's HTML structure)
        title = [headline.text for headline in soup.find_all("h2")]
        description = [article.text for article in soup.find_all("div")]

        # Return scraped headlines and articles
        print("Headline:\nArticle:", title, description)
        return title, description

    except Exception as e:
        print("Error occurred during scraping:", e)
        return [], []