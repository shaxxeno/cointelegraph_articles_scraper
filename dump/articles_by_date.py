"""THIS CODE DOES NOT WORK PROPERLY AND MAY CAUSE UNEXPECTED ISSUES(at least it works;))"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time


def get_source_page(url):
    global x
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url=url)
    time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    req_datetime_str = '2023-01-01'
    posts_more = driver.find_element(By.CLASS_NAME, 'posts-listing__navigation')
    get_datetime = soup.find('ul', class_='posts-listing__list').find_all('li', class_='posts-listing__item')
    for i in get_datetime:
        x = i.find('article', class_='post-card-inline').find('div', class_='post-card-inline__meta').find('time',
                                                                                                           class_='post-card-inline__date').get(
            'datetime')

    while True:
        if x <= req_datetime_str:
            with open('files/ex.html', 'w') as file:
                file.write(driver.page_source)
            break

        else:
            actions = ActionChains(driver=driver)
            actions.move_to_element(posts_more).perform()
            time.sleep(1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            get_datetime = soup.find('ul', class_='posts-listing__list').find_all('li', class_='posts-listing__item')
            for i in get_datetime:
                x = i.find('article', class_='post-card-inline').find('div', class_='post-card-inline__meta').find(
                    'time', class_='post-card-inline__date').get('datetime')

    articles_urls_list = []
    articles_urls = soup.find_all('a', class_='post-card-inline__title-link')
    for au in articles_urls:
        article_url = au.get('href')
        articles_urls_list.append(article_url)
    with open('../files/articles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'https://cointelegraph.com/{url}\n')


def main():
    get_source_page('https://cointelegraph.com/category/top-10-cryptocurrencies')


# if __name__ == '__main__':
#     main()
