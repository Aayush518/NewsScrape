
# NewsScrape

NewsScrape is a Python script that processes and beautifies news data from a JSON file. It extracts content from URLs, removes special characters, and rephrases the content for a cleaner presentation.

## Prerequisites

Make sure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Usage

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Aayush518/NewsScrape.git
    cd NewsScrape
    ```

2. **Prepare Your News Data:**

    Update the `updated_news_data.json` file with your news data. Each news item should have "headline," "content," and "summary" fields.

3. **Run the Script:**

    ```bash
    python generate_single.py
    ```

    This will process each news item, create individual text files, and store them in the project directory.

## File Structure

- `generate_single.py`: The main script to process news data.
- `rephrase.py`: Additional script for rephrasing content (optional).
- `updated_news_data.json`: JSON file containing news data.

## Generated Output

The script will create individual text files (e.g., `news_1.txt`, `news_2.txt`) for each news item with the original title and rephrased content.

