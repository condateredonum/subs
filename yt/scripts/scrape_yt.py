import os
from googleapiclient.discovery import build
from channel_info import get_channel_ids, get_usernames
from utils import save_to_md

API_KEY = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Channel ID curl
# curl "https://youtube.googleapis.com/youtube/v3/search?part=snippet&type=channel&q=2lazy2tryYT&key=API_KEY

# Username curl
# curl "https://youtube.googleapis.com/youtube/v3/channels?part=id&id=UCJjSDX-jUChzOEyok9XYRJQ&key=API_KEY

def get_latest_videos(channel_id_or_username):
    """Fetch the latest 3 videos from the provided channel ID or username."""
    if "youtube.com/channel/" in channel_id_or_username:
        # If it's a channel ID, use it directly.
        channel_id = channel_id_or_username.split("/")[-1]  # Get the last part after "/channel/"
    elif "youtube.com/@" in channel_id_or_username:
        # For usernames, we need to fetch the channel ID first
        username = channel_id_or_username.split('/')[-1]  # Extract the username correctly
        request = youtube.search().list(  # Change to search instead of channels
            part='snippet',
            type='channel',  # Ensure we're searching for channels
            q=username  # Search using the username
        )
        response = request.execute()
        
        # Extract the channel ID
        if response['items']:
            channel_id = response['items'][0]['id']['channelId']  # Get the channelId from snippet
        else:
            return []  # Return empty if no channel found
    else:
        return []  # Invalid input format

    # Fetch the latest videos for the channel ID
    response = youtube.search().list(
        channelId=channel_id,
        part='id,snippet',
        order='date',
        maxResults=3
    ).execute()

    video_list = []
    for item in response['items']:
        # Ensure the item is of type "video" before accessing videoId
        if item['id']['kind'] == 'youtube#video':
            video_list.append({
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })
    return video_list

def scrape_videos(md_file_path):
    """Scrape videos for both channel IDs and usernames."""
    channel_ids = get_channel_ids(md_file_path)
    usernames = get_usernames(md_file_path)
    
    all_videos = {}

    # Scrape videos for channel IDs
    for channel_id in channel_ids:
        videos = get_latest_videos(f"https://www.youtube.com/channel/{channel_id}")
        all_videos[channel_id] = videos
    
    # Scrape videos for usernames
    for username in usernames:
        videos = get_latest_videos(f"https://www.youtube.com/@{username}/videos")
        all_videos[username] = videos
    
    return all_videos

if __name__ == "__main__":
    # Specify your Markdown file path
    # channel_ids_file = 'yt/subs.md'
    # output_path='yt/latest.md'
    channel_ids_file = 'yt/test.md'
    output_path='yt/test_latest.md'

    videos = scrape_videos(channel_ids_file)
    
    # Optionally, save or format the output
    save_to_md(videos, file_path=output_path)