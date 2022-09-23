from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from .standard_auth_backend import StandardAuthBackend
from loguru import logger


username_input_xpath = '//*[@id="loginForm"]/div/div[1]/div/label/input'
password_input_xpath = '//*[@id="loginForm"]/div/div[2]/div/label/input'
login_button_xpath = '//*[@id="loginForm"]/div/div[3]/button'
error_field_xpath = '//*[@id="slfErrorAlert"]'

class InstagramBackend(StandardAuthBackend):
    def __init__(self, chrome_binary_path, chrome_version) -> None:
        super().__init__()
        self.chrome_location = chrome_binary_path
        self.chrome_version = chrome_version

    async def validate_impl(self, username, password):
        webdriver_options = webdriver.ChromeOptions()
        webdriver_options.binary_location = self.chrome_location
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=self.chrome_version).install()), options = webdriver_options)
        
        driver.get("https://www.instagram.com/")


        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'loginForm')))
    
        driver.find_element(By.XPATH, "/html/body/div[4]/div/div/button[1]").click() # close cookies
        time.sleep(1)
        driver.find_element(By.XPATH, username_input_xpath).send_keys(username)
        time.sleep(1)
        driver.find_element(By.XPATH, password_input_xpath).send_keys(password)
        time.sleep(1)

        driver.find_element(By.XPATH, login_button_xpath).click()


        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, error_field_xpath)))
            driver.find_element(By.XPATH,error_field_xpath)
            return False
        except Exception:
            try:
                # Try to retrieve the first post, if the user is logged in
                driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/section/div/div[2]/div')
                
                return True
            except:
                return driver.current_url != "https://www.instagram.com/"
