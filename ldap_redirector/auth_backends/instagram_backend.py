import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time

username_input_xpath = '//*[@id="loginForm"]/div/div[1]/div/label/input'
password_input_xpath = '//*[@id="loginForm"]/div/div[2]/div/label/input'
login_button_xpath = '//*[@id="loginForm"]/div/div[3]/button'
error_field_xpath = '//*[@id="slfErrorAlert"]'

async def validate(username, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    driver.get("https://www.instagram.com/")

    driver.find_element_by_xpath(username_input_xpath).send_keys(username)
    time.sleep(.2)
    driver.find_element_by_xpath(password_input_xpath).send_keys(password)
    time.sleep(.2)

    driver.find_element_by_xpath(login_button_xpath).click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath(error_field_xpath)
        return False
    except selenium.NoSuchElementException:
        return True

