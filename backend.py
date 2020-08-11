import requests
from bs4 import BeautifulSoup

def request(url):
    response = requests.get(url)
    return response

def get_main_page():
    html = request('https://youtube.com/').content
    #print(html)
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all(id='video-title')
    print(titles)

get_main_page()