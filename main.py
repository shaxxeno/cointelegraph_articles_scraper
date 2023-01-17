import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests


def get_source_page(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url=url)
    time.sleep(2)

    # scroll to the very bottom of the page
    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    count = 0
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        count += 1
        print(f'RickScrolled {count} times...')
        if screen_height * i > scroll_height:
            break

    # save articles urls in a file
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    articles_urls_list = []
    articles_urls = soup.find_all('a', class_='post-card-inline__title-link')
    for au in articles_urls:
        article_url = au.get('href')
        articles_urls_list.append(article_url)
    with open('files/articles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'https://cointelegraph.com/{url}\n')


def get_data(file_path):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
    }
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]

    s = requests.Session()
    result_data = []
    for url in urls_list[:3]:
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1', class_='post__title').text.strip()
        publish_date = soup.find('div', class_='post-meta__publish-date').find('time').text.strip()
        try:
            post_lead = soup.find('div', class_='post__block post__block_lead-text').find('p', class_='post__lead').text.strip()
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
    with open('files/result.json', 'w') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    get_source_page('https://cointelegraph.com/tags/business')
    get_data('files/articles_urls.txt')


if __name__ == '__main__':
    main()
