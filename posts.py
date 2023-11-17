import json

def format_news_post(news_data):
    formatted_posts = []

    for index, news_item in enumerate(news_data, start=1):
        headline = news_item["headline"]
        content = news_item["content"]

        post = f"**News {index}: {headline}**\n\n{content}\n\n{'='*50}\n"
        formatted_posts.append(post)

    return formatted_posts

def print_formatted_posts(formatted_posts):
    for post in formatted_posts:
        print(post)

if __name__ == "__main__":
    # Load news data from the JSON file
    with open('news_data.json', 'r', encoding='utf-8') as json_file:
        news_data = json.load(json_file)

    # Format news posts
    formatted_posts = format_news_post(news_data)

    # Print formatted posts
    print_formatted_posts(formatted_posts)
