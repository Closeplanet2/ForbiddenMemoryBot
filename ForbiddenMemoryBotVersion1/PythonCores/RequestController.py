import requests
from bs4 import BeautifulSoup
import time


def download_image(image_url, save_path, verify=True):
    pull_image = requests.get(image_url, verify=verify)
    with open(save_path, 'wb') as handler:
        handler.write(pull_image.content)


def pull_website(webpage_url, sleep=1, use_soup=True):
    page = requests.get(webpage_url)
    time.sleep(sleep)
    return BeautifulSoup(page.text, "html.parser") if use_soup else page.text
