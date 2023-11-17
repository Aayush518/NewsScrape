import json
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.data import find
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
download('punkt')
download('wordnet')
download('stopwords')

# Load NLTK resources
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def remove_special_characters(text):
    # Remove special characters and digits using regex
    return ''.join(e for e in text if (e.isalpha() or e.isspace()))


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
    # Use the "content" field directly
    content = news.get('content', '')

    # Remove special characters and digits
    clean_content = remove_special_characters(content)

    # Rephrase the content
    rephrased_content = rephrase(clean_content)

    # Update the news object with rephrased content
    news['rephrased_content'] = rephrased_content

if __name__ == "__main__":
    # Load your news data from the JSON file
    with open('updated_news_data.json', 'r') as file:
        news_data = json.load(file)

    # For each news item, process and print the results
    for i, news_item in enumerate(news_data, start=1):
        process_news(news_item)

        # Create individual files for each news item
        filename = f'news_{i}.txt'
        with open(filename, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Original Title: {news_item['headline']}\n")
            output_file.write(f"Rephrased Content: {news_item['rephrased_content']}\n")
