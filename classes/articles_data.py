import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from classes.selenium_scroll import AutoScroll

load_dotenv()


class Data:

    def __init__(self, file_path):
        self.file_path = file_path
        self.auto = AutoScroll(os.getenv('LINK'))

    def save_urls(self):
        soup = BeautifulSoup(self.auto.page_source, 'html.parser')
        articles_urls = soup.find_all('a', class_='post-card-inline__title-link')
        articles_urls_list = []
        for au in articles_urls:
            article_url = au.get('href')
            articles_urls_list.append(article_url)
        with open('../files/articles_urls.txt', 'w') as file:
            for url in articles_urls_list:
                file.write(f'https://cointelegraph.com/{url}\n')

    def get_data(self):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        with open(self.file_path) as file:
            urls_list = [line.strip() for line in file.readlines()]

        s = requests.Session()
        result_data = []
        for url in urls_list:
            response = s.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.find('h1', class_='post__title').text.strip()
            publish_date = soup.find('div', class_='post-meta__publish-date').find('time').text.strip()
            try:
                post_lead = soup.find('div', class_='post__block post__block_lead-text').find('p',
                                                                                              class_='post__lead').text.strip()
                img_url = soup.find('div', class_='post-cover post__block').find('picture').find('img').get('srcset')
            except Exception:
                post_lead = 'no_data'
                img_url = 'no_data'

            result_data.append({
                'url': url,
                'title': title,
                'publish_date': publish_date,
                'post_lead': post_lead,
                'img_url': img_url
            })

        with open('../files/result.json', 'w') as file:
            json.dump(result_data, file, indent=4, ensure_ascii=False)
        return f'../files/result.json'

# data = Data('../files/articles_urls.txt')
# data.save_urls()
# data.get_data()
