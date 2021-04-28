#!/usr/bin/env python3
# https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug
from contextlib import contextmanager


from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from fake_useragent import UserAgent
from selenium.webdriver import Chrome, Firefox, FirefoxProfile

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from core.web.scraper.exceptions.webscraper_error import WebScraperContentError
from os.path import abspath
from logger.logger_master import tracker_scraper_logger
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib3.exceptions import ReadTimeoutError
import time
from keyboard import send
CHROME_DRIVER_PATH = abspath('./bin/windows/chromedriver.exe')
FIREFOX_DRIVER_PATH = abspath('./bin/windows/geckodriver.exe')


import socket


# // ChromeDriver is just AWFUL because every version or two it breaks unless you pass cryptic arguments
# //AGRESSIVE: options.setPageLoadStrategy(PageLoadStrategy.NONE); // https://www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer-selenium.html
# options.addArguments("start-maximized"); // https://stackoverflow.com/a/26283818/1689770
# options.addArguments("enable-automation"); // https://stackoverflow.com/a/43840128/1689770
# options.addArguments("--headless"); // only if you are ACTUALLY running headless
# options.addArguments("--no-sandbox"); //https://stackoverflow.com/a/50725918/1689770
# options.addArguments("--disable-infobars"); //https://stackoverflow.com/a/43840128/1689770
# options.addArguments("--disable-dev-shm-usage"); //https://stackoverflow.com/a/50725918/1689770
# options.addArguments("--disable-browser-side-navigation"); //https://stackoverflow.com/a/49123152/1689770
# options.addArguments("--disable-gpu"); //https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

from time import sleep

class BrowserDriver:
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # options.add_argument('--user-data-dir=chrome-data')

    def get(self, url, timeout=10):
        try:
            user_agent = UserAgent()
            chrome_options = Options()
            chrome_options.add_argument(f'user-agent={user_agent.random}')
            chrome_options.headless = True
            chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
            chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2})
            chrome_options.add_experimental_option("prefs", {'profile.default_content_settings.images': 2})

            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-browser-side-navigation")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-javascript")

            socket.setdefaulttimeout(30)
            sleep(0.5)
            with Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options) as browser_driver:
                tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: (GET) [ {url} ]')

                actions = ActionChains(browser_driver)
                browser_driver.set_page_load_timeout(timeout)
                browser_driver.get(url)

                actions.send_keys(Keys.ESCAPE)
                actions.perform()

                response = browser_driver.page_source
                browser_driver.close()
                browser_driver.quit()
            return response

        except Exception as error:
            tracker_scraper_logger.logger.warning(f'{self.__class__.__name__}: WebDriverTimeout: {error}')
            return ''
