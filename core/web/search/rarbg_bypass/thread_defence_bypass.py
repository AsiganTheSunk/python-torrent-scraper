import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from .captcha_handler import CaptchaHandler

chrome_options = ChromeOptions()


chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

firefox_options = FireFoxOptions()
firefox_options.add_argument('--headless')
firefox_options.add_argument("--disable-gpu")
firefox_options.binary_location = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'


class ThreatDefenceBypass:
    """
    Custom RedirectMiddleware
    Using Selenium and chromedriver with a --headless flag
    Checks if redirected to a CAPTCHA page or a browser identification page and acts accordingly
    """
    def __init__(self):
        self.threat_defence = 'threat_defence.php'
        self.driver = webdriver.Chrome(r"chromedriver.exe",chrome_options=chrome_options)
        #self.driver = webdriver.Firefox('C:\\logger\\geckodriver\\geckodriver.exe',firefox_options=firefox_options)
        self.tries = 0
        self.captcha_handler = CaptchaHandler()
        self.cookies = None

    def bypass_threat_defense(self, url):
        time.sleep(3)
        # LOGGER.info('Number of tries: #{0}'.format(self.tries))
        self.driver.get(url)
        # While loop to decide whether we are on a browser detection (redirect) page or a captcha page
        while self.tries <= 5:  # Current limit is 5 giving pytesseract % of success
            print('Waiting for browser detection')
            time.sleep(3)
            try:
                self.cookies = self.find_solve_submit_captcha()
                break
            except NoSuchElementException:
                print()
                print('No CAPTCHA found in page')
            try:
                self.redirect_retry()
                break
            except NoSuchElementException:
                print('No Link in page either. EXITING')
                break
        # If the solution was wrong and we are prompt with another try call method again
        if self.threat_defence in self.driver.current_url:
            self.tries += 1
            # LOGGER.info('CAPTCHA solution was wrong. Trying again')
            self.bypass_threat_defense(self.driver.current_url)
        if self.cookies:
            self.driver.close()
            return self.cookies
        exit('Something went wrong')

    # Press retry link if reached a redirect page without captcha
    def redirect_retry(self):
        # LOGGER.info('Looking for `retry` link in page')
        link = self.driver.find_element_by_partial_link_text('Click')
        # LOGGER.info('Retrying to get CAPTCHA page')
        self.tries += 1
        self.bypass_threat_defense(link.get_attribute('href'))

    def find_solve_submit_captcha(self):
        # LOGGER.info('Looking for CAPTCHA image in page')
        # Find
        captcha = self.driver.find_element_by_xpath("//img[contains(@src, 'captcha')]")
        # LOGGER.info('Found CAPTCHA image: {0}'.format(captcha.get_attribute('src')))
        # Solve
        solved_captcha = self.captcha_handler.get_captcha(src=captcha.get_attribute('src'))
        # LOGGER.info('CAPTCHA solved: {0}'.format(solved_captcha))
        input_field = self.driver.find_element_by_id('solve_string')
        input_field.send_keys(solved_captcha)
        # LOGGER.info('Submitting solution')
        # Submit
        self.driver.find_element_by_id('button_submit').click()
        return self.driver.get_cookies()
