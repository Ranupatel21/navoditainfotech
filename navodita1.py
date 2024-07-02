import requests
from bs4 import BeautifulSoup

def get_news_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    
    for item in soup.find_all('div', class_='news-article'):
        title = item.find('h2').text
        date = item.find('time')['datetime']
        content = item.find('p').text
        
        articles.append({
            'title': title,
            'date': date,
            'content': content
        })
    
    return articles

url = 'https://example-news-website.com'
news_articles = get_news_articles(url)
