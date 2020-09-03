#!/usr/bin/env python
import os
import requests
import json 
import video_class

def search(query):

    headers = {
    'Accept': 'application/json',
    }

    params = (
    ('part', 'snippet'),
    ('maxResults', '25'),
    ('q', query),
    ('key', os.environ.get('YOUTUBE_KEY')),
    )

    response = requests.get('https://www.googleapis.com/youtube/v3/search', headers=headers, params=params).json()
    payload = []
    for i in response['items']:
        print(i)
        try:
            payload.append(video_class.YtVideo(i['snippet']['title'], i['snippet']['channelTitle'], "https://www.youtube.com/watch?v=" + i['id']['videoId'] ))
        except KeyError:
            print("Key error, probably not a video")

    return payload 

def main_page(region):
    print("MAIN PAGE: \n\n")
    headers = {
    'Accept': 'application/json',
    }

    params = (
    ('part', 'snippet,contentDetails,statistics'),
    ('chart', 'mostPopular'),
    ('regionCode', region),
    ('key', os.environ.get('YOUTUBE_KEY')),
    )

    response = requests.get('https://www.googleapis.com/youtube/v3/videos', headers=headers, params=params).json()
    payload = []
    for i in response['items']:
        print(i)
        print("\n")
        try:
            payload.append(video_class.YtVideo(i['snippet']['title'], i['snippet']['channelTitle'], "https://www.youtube.com/watch?v=" + i['id'] ))
        except KeyError:
            print("Key error, probably not a video")

    return payload 

print(len(search("minecraft")))
print(main_page("US"))
