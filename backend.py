import requests
from bs4 import BeautifulSoup

def request(url):
    response = requests.get(url)
    return response

def get_main_page():
    html = request('https://www.youtube.com/').content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    print(soup.find_all("a", id="video-title-link"))

get_main_page()