import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()


class AutoScroll:
    def __init__(self, url):
        self.page_source = None
        self.url = url
        self.scroll()

    def scroll(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.get(url=self.url)
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
            # if count % 5 == 0:
            #     print(f'RickScrolled {count} times...')
            if screen_height * i > scroll_height:
                break
        self.page_source = driver.page_source
