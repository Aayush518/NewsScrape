import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from newspaper import Article

def scrape_news(url, num_articles=10):
    news_data = []

    # Initialize a headless browser (make sure you have the appropriate driver installed)
    browser = webdriver.Chrome()  # You can replace with the path to your webdriver if needed

    try:
        # Open the URL
        browser.get(url)

        # Simulate scrolling to load more content
        for _ in range(num_articles // 10):  # Assuming 10 articles are loaded per scroll
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Allow time for content to load

        # Get the updated page source
        page_source = browser.page_source

        # Parse the HTML content of the updated page using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the elements containing news headlines and links
        articles = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')

        # Collect the headlines and full news content
        for article in articles[:num_articles]:
            article_url = article['href']
            full_article = get_full_article_content(article_url, base_url="https://www.bbc.com")
            news_data.append({
                "headline": article.text.strip(),
                "content": full_article
            })

    finally:
        # Close the browser
        browser.quit()

    return news_data

def get_full_article_content(article_url, base_url):
    # Check if the article_url is already an absolute URL
    if article_url.startswith(('http://', 'https://')):
        full_url = article_url
    else:
        full_url = f"{base_url}{article_url}"

    article = Article(full_url)
    
    try:
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error parsing the article: {str(e)}"


def save_to_json(data, filename='news_data.json'):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # URL of the BBC News website
    bbc_news_url = "https://www.bbc.com/news"

    # Scrape news and save to JSON file
    news_data = scrape_news(bbc_news_url, num_articles=50)  # Adjust the number as needed
    save_to_json(news_data, filename='news_data.json')
