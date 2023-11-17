import json
from jinja2 import Environment, FileSystemLoader

# Load JSON data from the file
with open('news_data.json', 'r', encoding='utf-8') as file:
    news_data = json.load(file)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('news_template.html')

# Render the template with news data
output_html = template.render(news_list=news_data)

# Save the generated HTML to a file
with open('generated_news.html', 'w', encoding='utf-8') as output_file:
    output_file.write(output_html)

print("HTML file generated successfully!")
