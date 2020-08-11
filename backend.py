import requests
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox()


def request(url):
    response = driver.get(url)
    return response

def get_main_page():
    html = request('https://www.youtube.com/')
    titles = driver.get_element_by_name("a")
    titles = soup.find_all('a', id='video-title-link')['title']
    print(titles)

get_main_page()