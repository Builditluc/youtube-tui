from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
driver = webdriver.Firefox()



class YtVideo:
    def __init__(self, title_arg, creator_arg, url_arg):
        self.title = title_arg
        self.creator = creator_arg
        self.url = url_arg


def request(url):
    driver.get(url)

def webscrape(search: bool):
    titles_array = []
    urls_array = []
    creators_array = []

    # get creators
    creators = driver.find_elements_by_xpath("//a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
    i = 0
    for creator in creators:
        i += 1
        if search == True:
            print("we're searching")
            if (i % 2) != 0:
                print(creator.text)
                creators_array.append(creator.text)
        else:
            print(creator.text)
            creators_array.append(creator.text)

    urls = ""

    # get urls and titles
    if not search:
        urls = driver.find_elements_by_id("video-title-link")
    else:
         urls = driver.find_elements_by_id("video-title")
    for url in urls:
        urls_array.append(url.get_attribute("href"))
        titles_array.append(url.get_attribute("title"))
    
    # for some reason, the first index of the array, should be the last, so i remove it and append it immediatly
    titles_array.append(titles_array.pop(0))
    creators_array.append(creators_array.pop(0))
    urls_array.append(urls_array.pop(0))

    # Generate return value
    return_value = []
    for i in range(len(titles_array)):
        
        print(i)
        print(len(creators_array))
        return_value.append(YtVideo(titles_array[i - 1], creators_array[i - 1], urls_array[i - 1]))

    return return_value

def get_main_page():
    
    request('https://www.youtube.com/')
    
    return webscrape(False)


def search(text):
    # search_bar = driver.find_element_by_xpath("//input[@id='search']")
    # search_bar.send_keys(text)
    # search_bar.send_keys(Keys.RETURN)
    request("https://www.youtube.com/results?search_query=" + urllib.parse.quote(text))


    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-horizontal-card-list-renderer/div[1]/h2/ytd-rich-list-header-renderer/div/div[2]/yt-formatted-string[1]/span[2]"))
    )
    print("it loaded")
    #time.sleep(2)
    return webscrape(True)
        
    
    
#print(get_main_page())
for i in search("star wars squadrons"):
    print(i.title + " " + i.url + " " + i.creator)
#driver.quit()
