import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.data import find
from nltk import download
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import re
from urllib.parse import urljoin

# Download NLTK resources
download('punkt')
download('wordnet')
download('stopwords')

# Load NLTK resources
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def remove_special_characters(text):
    # Remove special characters and digits using regex
    return re.sub(r'[^a-zA-Z\s]', '', text)


def tokenize_and_lemmatize(text):
    words = word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in words]
    return lemmatized_words


def get_text_from_url(url):
    # Extract text content from the given URL
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([paragraph.get_text() for paragraph in paragraphs])
        return content
    except Exception as e:
        print(f"Error extracting content for {url}: {e}")
        return None


def rephrase(content):
    # Tokenize and lemmatize the content
    words = tokenize_and_lemmatize(content)

    # Remove stop words
    words = [word for word in words if word not in stop_words]

    # Detokenize the words to form a coherent sentence
    detokenized_text = TreebankWordDetokenizer().detokenize(words)

    return detokenized_text


def process_news(news):
    # Combine the news title and description
    full_text = f"{news['title']} {news['description']}"

    # Extract content from the URL
    content = get_text_from_url(news['url'])

    if content:
        # Remove special characters and digits
        clean_content = remove_special_characters(content)

        # Rephrase the content
        rephrased_content = rephrase(clean_content)

        # Update the news object with rephrased content
        news['rephrased_content'] = rephrased_content
    else:
        print(f"Error extracting content for {news['title']}: 'url'")


if __name__ == "__main__":
    # Load your news data from the JSON file
    with open('news_data.json', 'r') as file:
        news_data = json.load(file)

    # For each news item, process and print the results
    for news_item in news_data:
        process_news(news_item)
        print("Original Title:", news_item['title'])
        print("Rephrased Content:", news_item['rephrased_content'])
        print("\n")
