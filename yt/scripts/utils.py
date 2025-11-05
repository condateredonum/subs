import os
import re
from datetime import datetime
import pytz
from googleapiclient.discovery import build

# https://console.cloud.google.com
API_KEY = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)

def convert_timestamp(source_datetime, target_time='Europe/London'):
    """Convert to 'Europe/London' or alternative if specified."""
    try:
        # Parse the source datetime string into a datetime object
        utc_datetime = datetime.fromisoformat(source_datetime[:-1])
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)  # Set timezone to UTC

        # Convert to the target timezone
        target_timezone = pytz.timezone(target_time)
        target_datetime = utc_datetime.astimezone(target_timezone)

        return target_datetime.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return source_datetime

def thumbnail_parser(snippet):
    thumbnail_keys = ['maxres', 'standard', 'high', 'medium', 'default']
    for key in thumbnail_keys:
        try:
            # Attempt to retrieve the thumbnail URL
            return snippet['thumbnails'][key]['url']
        except (KeyError, IndexError):
            continue  # If this key fails, move to the next one

    return 'Thumbnail-Error'

def duration_to_seconds(time_str):
    """Convert string of format HH:MM:SS to seconds."""
    try:
        # Split the input string by the colon ':'
        hours, minutes, seconds = map(int, time_str.split(':'))

        # Calculate total seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
    except:
        total_seconds = 600

    return total_seconds

def convert_to_hhmmss(iso_duration):
    """Convert ISO 8601 duration string to format HH:MM:SS"""
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
    # https://youtube.googleapis.com/youtube/v3/playlistItems?
    # part=snippet&playlistId=UUZZHPXsg6LopvdOKF7qM6cQ&key=
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=num_videos
    )
    playlist_response = playlist_request.execute()

    return playlist_response

def save_to_md(all_videos, file_path='yt/latest.md'):
    """Save scraped video data to a Markdown file with a timestamp."""

    # Get the current timestamp
    timestamp = datetime.now(tz=pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    timestamp = convert_timestamp(timestamp)

    # Create the new content with the video data
    new_content = "-------------------\n"
    new_content += f"# {timestamp}\n\n"

    # Add the Markdown table header with the specified format
    new_content += "| Thumbnail | Title |\n"
    new_content += "|-----------|-------|\n"

    # Write the video data to the new content
    for video in all_videos:
        new_content += (
            f"|![]({video['Video Thumbnail']}) |"
            f"{video['Video Upload Date']}<br>"
            f"{video['Username']}<br>"
            f"[{video['Video Title']}](https://www.youtube.com/watch?v={video['Video ID']})<br>"
            f"[{video['Video Duration']}] |\n"
        )
    new_content += "-------------------\n"

    # Append the new content to the existing file
    if os.path.exists(file_path):
        with open(file_path, 'r+') as file:
            # existing_content = file.read()
            # file.seek(0) 
            # file.write(new_content + existing_content) 
            file.write(new_content)
    else:
        with open(file_path, 'w') as file:
            file.write(new_content)  # Create the file if it doesn't exist

    print(f"Data saved to {file_path}.")

if __name__ == "__main__":
    iso_duration = 'PT17M23S'
    convert_to_hhmmss(iso_duration)
