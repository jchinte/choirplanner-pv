# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import googleapiclient.discovery


def youtube_search(query):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDn1Uqd5Q8rhWyZNBMjxu1N5BWDXNRgc1M"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q=str(query),
        access_token="AIzaSyDn1Uqd5Q8rhWyZNBMjxu1N5BWDXNRgc1M",
        type="video",
    )
    response = request.execute()
    vids = [item['id']['videoId'] for item in response['items']]
    return vids[::-1]

def main():
    response = youtube_search("surfing")
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    print(response)

if __name__ == "__main__":
    main()