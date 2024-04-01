from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib3
import time


class WebsiteController:
    def __init__(self, full_screen=False, executable_path='C:\chromedriver\chromedriver.exe'):
        self.chrome_driver = webdriver.Chrome(executable_path=executable_path)
        if full_screen:
            self.chrome_driver.maximize_window()
        urllib3.disable_warnings()

    def return_webpage(self, webpage_url, sleep=1):
        self.chrome_driver.get(webpage_url)
        time.sleep(sleep)
        return self.update_webpage()

    def return_element(self, class_name=None, id_name=None):
        if not class_name is None:
            return self.chrome_driver.find_element(By.CLASS_NAME, class_name)
        else:
            return self.chrome_driver.find_element(By.ID, id_name)

    def click_element(self, class_name=None, id_name=None, sleep=1):
        self.return_element(class_name, id_name).click()
        time.sleep(sleep)
        return self.update_webpage()

    def send_keys_to_element(self, input_value, class_name=None, id_name=None, sleep=1):
        self.return_element(class_name, id_name).send_keys(input_value)
        time.sleep(sleep)
        return self.update_webpage()

    def clear_element(self, class_name=None, id_name=None, sleep=1):
        self.return_element(class_name, id_name).clear()
        time.sleep(sleep)
        return self.update_webpage()

    def update_webpage(self):
        return BeautifulSoup(self.chrome_driver.page_source, "html.parser")
