# yt/scripts/utils.py
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

def api_get_video_duration(video_id):
    # https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id=0pUlHrVNZqA&key=
    video_content_request = youtube.videos().list(
        part='contentDetails',
        id=video_id
    )
    video_content_response = video_content_request.execute()
    try:
        if video_content_response['items']:
            video_duration = video_content_response['items'][0]['contentDetails']['duration']
        else:
            video_duration = 'Live'
    except (IndexError, KeyError):
        video_duration = 'Duration-Error'
    
    return video_duration
