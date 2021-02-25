from selenium import webdriver
import os


def init_browser() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(executable_path=f"{os.getcwd()}\\lib\\chromedriver.exe", options=chrome_options)

    return browser
