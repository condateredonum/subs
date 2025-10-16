import re
import os
from datetime import datetime
from googleapiclient.discovery import build

# https://console.cloud.google.com
API_KEY = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)

def save_to_md(videos, file_path='yt/latest.md'):
    """Save scraped video data to a Markdown file with a timestamp."""

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Open the file in write mode, overwriting it each time
    with open(file_path, 'w') as file:
        # Write the timestamp at the top
        file.write(f"Last updated: {timestamp}\n\n")
        file.write(f"# Latest Videos\n")
        
        # Write the video data
        for channel, video_list in videos.items():
            file.write(f"## Videos from {channel}\n")
            for video in video_list:
                file.write(f"- [{video['title']}]({video['url']})\n")
            file.write("\n")  # Add a newline between channels

def convert_to_hhmmss(iso_duration):
    """Conver ISO 8601 duration string to format HH:MM:SS"""
    # Updated regex: Makes both hours and minutes completely optional
    # match = re.match(r'PT(?:(\d+H)?(?![^M])|(?:\d+M)?|(?:\d+S))', iso_duration)
    # if match is None:
    #     video_duration = iso_duration

    try:
        hours_match = re.search(r'(\d+)H', iso_duration)
        minutes_match = re.search(r'(\d+)M', iso_duration)
        seconds_match = re.search(r'(\d+)S', iso_duration)

        hours = int(hours_match.group(1)) if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        seconds = int(seconds_match.group(1)) if seconds_match else 0
        print(f'\t\tHours: {hours} Minutes: {minutes} Seconds: {seconds}')
        video_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except:
        video_duration = iso_duration

    return video_duration

def api_get_video_duration(video_id):
    """Get the video duration from the unique video ID."""
    # https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id=0pUlHrVNZqA&key=
    video_content_request = youtube.videos().list(
        part='contentDetails',
        id=video_id
    )
    video_content_response = video_content_request.execute()
    try:
        if video_content_response['items']:
            video_duration = video_content_response['items'][0]['contentDetails']['duration']
            video_duration = convert_to_hhmmss(video_duration)
        else:
            video_duration = 'Live'
    except (IndexError, KeyError):
        video_duration = 'Duration-Error'
    
    return video_duration


def api_get_playlist_items(uploads_playlist_id, num_videos=2):
    """Get the video duration from the unique video ID."""
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=num_videos
    )
    playlist_response = playlist_request.execute()

    return playlist_response


if __name__ == "__main__":
    iso_duration = 'PT17M23S'
    convert_to_hhmmss(iso_duration)