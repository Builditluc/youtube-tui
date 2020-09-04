#!/usr/bin/env python
import os
import requests
import json 
import video_class

def search(query, api_key):

    headers = {
    'Accept': 'application/json',
    }

    params = (
    ('part', 'snippet'),
    ('maxResults', '25'),
    ('q', query),
    ('key', api_key
    ))

    response = requests.get('https://www.googleapis.com/youtube/v3/search', headers=headers, params=params)
    if response.status_code == 200:
        response = response.json()
        payload = []
        for i in response['items']:
            print(i)
            try:
                payload.append(video_class.YtVideo(i['snippet']['title'], i['snippet']['channelTitle'], "https://www.youtube.com/watch?v=" + i['id']['videoId'] ))
            except KeyError:
                print("Key error, probably not a video")

        return payload 
    else:
        raise Exception("api didn't return status code 200, throwing an error")
    
def main_page(region, api_key):
    #print("MAIN PAGE: \n\n")
    headers = {
    'Accept': 'application/json',
    }

    params = (
    ('part', 'snippet,contentDetails,statistics'),
    ('chart', 'mostPopular'),
    ('regionCode', region),
    ('key', api_key
    ))

    response = requests.get('https://www.googleapis.com/youtube/v3/videos', headers=headers, params=params)
    if response == 200:
        response = response.json()
        payload = []
        for i in response['items']:
            print(i)
            print("\n")
            try:
                payload.append(video_class.YtVideo(i['snippet']['title'], i['snippet']['channelTitle'], "https://www.youtube.com/watch?v=" + i['id'] ))
            except KeyError:
                print("Key error, probably not a video")

        return payload 
    else:
        raise Exception("api didn't return status code 200, throwing an error")
print(search("minecraft"), os.environ.get("YOUTUBE_KEY"))
#print(main_page("US"))
