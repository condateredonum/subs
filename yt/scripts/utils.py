# yt/scripts/utils.py

def save_to_md(videos):
    """Save scraped video data to a Markdown file."""
    with open('latest_videos.md', 'w') as file:
        for channel, video_list in videos.items():
            file.write(f"## Videos from {channel}\n")
            for video in video_list:
                file.write(f"- [{video['title']}]({video['url']})\n")
            file.write("\n")  # Add a newline between channels
