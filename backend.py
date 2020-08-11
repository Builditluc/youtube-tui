import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

driver = webdriver.Firefox()


def request(url):
    driver.get(url)
    #return response

def get_main_page():
    titles_array, urls_array,  creators_array = [], [], []
    request('https://www.youtube.com/')
    
    # get titles
    titles = driver.find_elements_by_id("video-title")
    for title in titles:
            titles_array.append(title.text)
    #print(titles_array)

    # get creators
    creators = driver.find_elements_by_id("channel-name")
    for creator in creators:
        creators_array.append(creator.text)
    #print(creators_array)

    # get urls
    urls = driver.find_elements_by_id("video-title-link")
    for url in urls:
        urls_array.append(url.get_attribute("href"))
    #print(urls_array)

    # generate json

    json_string = [{"title": t, "creator": s, "url": x} for t, s, x in zip(titles_array, creators_array, urls_array)]
        
    json_to_return = json.dumps(json_string)
    
    #print(json_to_return)
    #print(len(json_to_return))
    
    for i in range(len(json.loads(json_to_return))):
        
        if json.loads(json_to_return)[i ]['title'] == "":
            print(i)
            
            
            print( json.loads(json_to_return)[i])
    
    print(json_to_return)
    
    return json_to_return

get_main_page()
driver.close()

def search(text):
    pass