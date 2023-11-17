import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from newspaper import Article
import spacy

# Download spaCy model
spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

def extract_text(url):
    # Extract text content from the article URL
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def summarize_and_rephrase(text):
    # Use spaCy to create a summary and rephrase sentences
    doc = nlp(text)
    summary = " ".join(sent.text for sent in doc.sents[:2])  # Summarize the first two sentences
    rephrased_content = " ".join(sent.text for sent in doc.sents[2:])  # Rephrase the remaining sentences
    return summary, rephrased_content

def generate_news_posts(news_list):
    for news in news_list:
        print(f"Processing: {news['headline']}")
        # Extract text content from the article URL
        try:
            content = extract_text(news['url'])
        except Exception as e:
            print(f"Error extracting content for {news['headline']}: {e}")
            continue

        # Summarize and rephrase the content
        summary, rephrased_content = summarize_and_rephrase(content)

        # Update the news dictionary
        news['summary'] = summary
        news['rephrased_content'] = rephrased_content

    return news_list

if __name__ == "__main__":
    # Load news data from JSON file
    with open("news_data.json", "r") as file:
        news_data = json.load(file)

    # Generate news posts with additional information
    updated_news_data = generate_news_posts(news_data)

    # Save the updated news data
    with open("updated_news_data.json", "w") as file:
        json.dump(updated_news_data, file, indent=2)

    print("News posts generated and saved.")
