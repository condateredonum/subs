import os
import json
import datetime
from utils import (
    convert_timestamp,
    thumbnail_parser,
    duration_to_seconds,
    url_to_html,
    api_get_playlist_items,
    api_get_video_duration,
    save_to_md
)

def get_channel_info(channel_info_file_path):
    """Fetch the Username and Uploads Playlist ID associated."""
    print('\nRunning: get_channel_info')
    with open(channel_info_file_path, 'r') as file:
        data = json.load(file)
        return data

def get_latest_videos(channel_data):
    """Fetch the latest x videos from a certain playlist"""
    print('\nRunning: get_latest_videos')
    all_videos = []

    for channel in channel_data:
        print(f'='*10)
        username = channel['username']
        print(f'Username: \t{username}')

        uploads_playlist_id = channel['uploads_playlist_id']
        print(f'Uploads ID: \t{uploads_playlist_id}')

        try:
            playlist_response = api_get_playlist_items(uploads_playlist_id)
            playlist_items = playlist_response['items']
        except:
            print(f'\t Error parsing playlist: {uploads_playlist_id}')
            continue

        if playlist_items:
            for playlist_video in playlist_items:
                snippet = playlist_video['snippet']
                video_thumbnail = thumbnail_parser(snippet)

                username = url_to_html(username)
                video_upload_date = snippet['publishedAt']
                video_upload_date = convert_timestamp(video_upload_date)
                video_title = snippet['title'].replace('|', '&#124;')
                video_id = snippet['resourceId']['videoId']
                video_duration = api_get_video_duration(video_id)

                duration_seconds = duration_to_seconds(video_duration)

                if duration_seconds > 120:
                    video_info = {
                        'Username': username,
                        'Video Title': video_title,
                        'Video Upload Date': video_upload_date,
                        'Video ID': video_id,
                        'Video Duration': video_duration,
                        'Video Thumbnail': video_thumbnail
                    }
                    all_videos.append(video_info)

                    print(f'\tTitle: \t\t {video_title}')
                    print(f'\tUpload Date: \t {video_upload_date}')
                    print(f'\tID: \t\t {video_id}')
                    print(f'\tDuration: \t {video_duration}')
                    print(f'\tThumbnail: \t {video_thumbnail} \n')
        else:
            return print('No videos found for {username}')

    all_videos = sorted(
        all_videos,
        key=lambda x: x['Video Upload Date'],
        reverse=True
    )

    return all_videos

if __name__ == "__main__":
    channel_info_file_path = 'yt/data/channel_info.json'
    channel_data = get_channel_info(channel_info_file_path)

    all_videos = get_latest_videos(channel_data)


    output_path='yt/markdowns/latest_videos.md'
    save_to_md(all_videos, file_path=output_path)
