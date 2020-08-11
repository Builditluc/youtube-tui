import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox()


def request(url):
    response = driver.get(url)
    return response

def get_main_page():
    html = request('https://www.youtube.com/')
    titles = driver.find_elements_by_id("video-title")
    print(titles)

get_main_page()


def search(text):
    pass