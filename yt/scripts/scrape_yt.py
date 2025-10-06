import os
from googleapiclient.discovery import build

API_KEY = 'YOUR_YOUTUBE_API_KEY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_latest_videos(channel_id):
    response = youtube.search().list(
        channelId=channel_id,
        part='id,snippet',
        order='date',
        maxResults=3
    ).execute()

    video_list = []
    for item in response['items']:
        video_list.append({
            'title': item['snippet']['title'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })
    return video_list

# Example: Replace 'YOUR_CHANNEL_ID' with the actual channel ID you want to scrape
if __name__ == "__main__":
    print(get_latest_videos('YOUR_CHANNEL_ID'))
