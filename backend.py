import requests
from bs4 import BeautifulSoup

def request(url):
    response = requests.get(url)
    return response

def get_main_page():
    html = request('https://www.youtube.com/').content
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    titles = soup.find_all("yt-formatted-string")
    print(titles)

get_main_page()