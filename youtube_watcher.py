#!/usr/bin/env python

import logging
from pprint import pformat 
import sys
import requests
import json
from config import config

key = config['google_api_key'] 
yt_playlist_id = config['youtube_playlist_id']

# to get all playlist info
def fetch_playlist_items_page(gapi_key, playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
    "key":gapi_key,
    "playlistId":playlist_id,
    "part":"contentDetails",
    "pageToken":page_token
    })
    payload = json.loads(response.text)
    return payload

# get videos page
def fetch_videos_page(gapi_key, video_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
    "key":gapi_key,
    "id":video_id,
    "part":"snippet,statistics",
    "pageToken":page_token
    })
    payload = json.loads(response.text)
    return payload

# fetch info 
def fetch_videos(key, playlist_id, page_token= None):
    payload = fetch_videos_page(key,playlist_id,page_token)

    yield from payload['items']

    next_page_token = payload.get('nextPageToken')

    if next_page_token is not None:
        yield from fetch_videos(key, playlist_id, next_page_token)   

# to get relevent fields from data
def summarize_video(video):
    return {
        "video_id":video["id"],
        "title":video["snippet"]['title'],
        "views":int(video["statistics"].get("viewCount")),
        "likes":int(video["statistics"].get("likeCount")),
        "comments":int(video["statistics"].get("commentCount")),
    } 



def fetch_playlist_items(google_api_key, playlist_id, page_token = None):
    payload = fetch_playlist_items_page(google_api_key,playlist_id,page_token)

    yield from payload['items']

    next_page_token = payload.get('nextPageToken')

    if next_page_token is not None:
        yield from fetch_playlist_items(google_api_key, yt_playlist_id, next_page_token)       



def main():
    logging.info("START")

    for video_item in fetch_playlist_items(key, yt_playlist_id):
        video_id = video_item['contentDetails']['videoId']
        for video in fetch_videos(key, video_id):
            logging.info(f"GOT {pformat(summarize_video(video))}")



if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
    # main()
