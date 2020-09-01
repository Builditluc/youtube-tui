
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options

import urllib.parse
import time
import os


#if os.environ.get("DEBUG_YOUTUBE_TUI") != "True":
#    options.headless = True
try:
    options = webdriver.firefox.options.Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
except FileNotFoundError:
    try:
        options = webdriver.chrome.options.Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

    except FileNotFoundError:
        try:
            driver = webdriver.Safari()
        except FileNotFoundError:
            try:
                options = webdriver.ie.options.Options()
                options.headless = True
                driver= webdriver.Ie(options=options)
            except FileNotFoundError:
                print("No usable browser found.")
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
    creators = driver.find_elements_by_xpath(
        "//a[@class='yt-simple-endpoint style-scope yt-formatted-string']")
    i = 0
    for creator in creators:
        i += 1
        if search == True:
            #print("we're searching")
            if (i % 2) != 0:
                # print(creator.text)
                creators_array.append(creator.text)
        else:
            # print(creator.text)
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
        if i >= 20:
            break
        try:
            return_value.append(
                YtVideo(titles_array[i - 1], creators_array[i - 1], urls_array[i - 1]))
        except:
            break

    return return_value


def get_main_page():

    request('https://www.youtube.com/')

    return webscrape(False)


def search(text):
    request("https://www.youtube.com/results?search_query=" +
            urllib.parse.quote(text))

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=\"logo-icon-container\"]"))
    )
    try:
        driver.find_element_by_xpath(
            "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-background-promo-renderer")
    except:
        time.sleep(0.3)
        return webscrape(True)
    else:
        return "error"
