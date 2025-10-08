# yt/scripts/utils.py
from datetime import datetime

def save_to_md(videos, file_path='yt/latest_videos.md'):
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
