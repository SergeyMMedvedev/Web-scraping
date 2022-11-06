from bs4 import BeautifulSoup
from headers import HEADERS
import requests


BASE_URL = 'https://habr.com'
ALL_ARTICLES = BASE_URL + '/ru/all'
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'Nintendo Switch']


def get_links_list(articles):
    links = []
    for article in articles:
        header = article.find('h2')
        a = header.find(class_="tm-article-snippet__title-link")
        links.append(a['href'])
    return links


def keywords_in_text(text):
    for keyword in KEYWORDS:
        if text.find(keyword) != -1:
            return True


def get_post_date(soup):
    post_date_tag = soup.find('time')
    if post_date_tag:
        return post_date_tag['title']
    print('time tag not found!')


def get_post_header(soup):
    post_header_tag = soup.find('h1')
    if post_header_tag:
        return post_header_tag.find('span').text
    print('Header tag not found!')


if __name__ == '__main__':

    response = requests.get(ALL_ARTICLES, headers=HEADERS)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    articles = soup.find_all('article')
    links = get_links_list(articles)

    for link in links:
        url = BASE_URL + link
        response = requests.get(url, headers=HEADERS)
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        post = soup.find(id='post-content-body')
        text = post.text
        if keywords_in_text(text):
            post_date = get_post_date(soup)
            post_header = get_post_header(soup)
            print(f'{post_date} - {post_header} - {url}')
