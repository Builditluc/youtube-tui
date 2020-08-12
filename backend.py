import requests
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

class yt_video:
    def __init__(self, title_arg, creator_arg, url_arg):
        #global title
        #global creator
        #global url
        self.title = title_arg
        self.creator = creator_arg
        self.url = url_arg

def request(url):
    driver.get(url)
    #return response

def get_main_page():
    titles_array = []
    urls_array = []
    creators_array = []
    request('https://www.youtube.com/')
    
    # get titles
    titles = driver.find_elements_by_id("video-title")
    for title in titles:
            titles_array.append(title.text)
    

    # get creators
    creators = driver.find_elements_by_id("channel-name")
    for creator in creators:
        creators_array.append(creator.text)

    # get urls
    urls = driver.find_elements_by_id("video-title-link")
    for url in urls:
        urls_array.append(url.get_attribute("href"))
    

    return_value = []
    for i in range(len(titles_array)):
        if titles_array[i - 1] != "":
            return_value.append(yt_video(titles_array[i - 1], creators_array[i - 1], urls_array[i - 1]))

    return return_value

#print(get_main_page())

def search(text):
    pass

