#!/usr/bin/env python3
# https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import WebDriverException, TimeoutException
from fake_useragent import UserAgent
from core.web.scraper.exceptions.webscraper_error import WebScraperContentError
from os.path import abspath
from logger.logger_master import tracker_scraper_logger
import time

CHROME_DRIVER_PATH = abspath('./bin/windows/chromedriver.exe')


class BrowserDriver:
    def __init__(self):
        user_agent = UserAgent()
        self.user_agent = user_agent.random
        self.options = Options()
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.headless = True
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        # options.add_argument('--user-data-dir=chrome-data')

    def get(self, url, debounce_action_time=1, timeout=30):
        browser_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=self.options)
        try:
            # initiating the webdriver. Parameter includes the path of the webdriver.
            # driver = webdriver.Firefox(executable_path='./geckodriver.exe')
            tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: (GET) [ {url} ]')
            browser_driver.set_page_load_timeout(timeout)
            browser_driver.get(url)
            # Timer to ensure the search is loaded.
            return browser_driver.page_source

        except TimeoutException as error:
            tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: WebDriverTimeout: {error}')
        except WebDriverException as error:
            tracker_scraper_logger.logger.info(f'{self.__class__.__name__}: WebDriverException: {error}')
            raise WebScraperContentError('ChromeWebDriver', error.msg)
        except Exception as error:
            tracker_scraper_logger.logger.warning(f'{self.__class__.__name__}: {error}')

        finally:
            browser_driver.close()
