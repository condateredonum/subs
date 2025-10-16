import re
import os
from datetime import datetime
from googleapiclient.discovery import build

# https://console.cloud.google.com
API_KEY = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)

def save_to_md(all_videos, file_path='yt/latest.md'):
    """Save scraped video data to a Markdown file with a timestamp."""

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the new content with the video data
    new_content = "-------------------\n"
    new_content += f"Last updated: {timestamp}\n\n"
    new_content += f"# Latest Videos\n"
    
    # Add the Markdown table header with the specified format
    new_content += "| Username | Video Upload Date | Video Title  | Video Duration | Video Thumbnail |\n"
    new_content += "|----------|-------------------|--------------|----------------|-----------------|\n"

    # Write the video data to the new content
    for video in all_videos:
        new_content += (
            f"| {video['Username']} | "
            f"{video['Video Upload Date']} | "
            f"[{video['Video Title']}](https://www.youtube.com/watch?v={video['Video ID']}) | "
            f"{video['Video Duration']} | "
            f"[Thumbnail]({video['Video Thumbnail']}) |\n"
        )
    new_content += "-------------------\n"

    # Append the new content to the existing file
    if os.path.exists(file_path):
        with open(file_path, 'r+') as file:
            existing_content = file.read()
            file.seek(0) 
            file.write(new_content + existing_content) 
    else:
        with open(file_path, 'w') as file:
            file.write(new_content)  # Create the file if it doesn't exist

    print(f"Data saved to {file_path}.")

def convert_to_hhmmss(iso_duration):
    """Conver ISO 8601 duration string to format HH:MM:SS"""
    try:
        hours_match = re.search(r'(\d+)H', iso_duration)
        minutes_match = re.search(r'(\d+)M', iso_duration)
        seconds_match = re.search(r'(\d+)S', iso_duration)

        hours = int(hours_match.group(1)) if hours_match else 0
        minutes = int(minutes_match.group(1)) if minutes_match else 0
        seconds = int(seconds_match.group(1)) if seconds_match else 0
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

def api_get_playlist_items(uploads_playlist_id, num_videos=5):
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