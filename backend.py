from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

driver = webdriver.Firefox()


class YtVideo:
    def __init__(self, title_arg, creator_arg, url_arg):
        self.title = title_arg
        self.creator = creator_arg
        self.url = url_arg


def request(url):
    driver.get(url)


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
    
    # Generate return value
    return_value = []
    for i in range(len(titles_array)):
        if titles_array[i - 1] != "":
            return_value.append(YtVideo(titles_array[i - 1], creators_array[i - 1], urls_array[i - 1]))

    return return_value


def search(text):
    # search_bar = driver.find_element_by_xpath("//input[@id='search']")
    # search_bar.send_keys(text)
    # search_bar.send_keys(Keys.RETURN)
    request("https://www.youtube.com/results?search_query=" + urllib.parse.quote(text))

    try:
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='video-title']"))
        )
        print("it loaded")
        
        #results = driver.find_elements_by_xpath("//yt-formatted-string[@class='ytd-video-renderer']")
        for i in results:
            print(i.text)
    finally:
        driver.quit()
    
    
#get_main_page()
search("foobar")
driver.close()
