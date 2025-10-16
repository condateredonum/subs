import os
import json
import datetime
from utils import api_get_playlist_items, api_get_video_duration, save_to_md

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
        username = channel['username']
        print(f'Username: {username}')

        uploads_playlist_id = channel['uploads_playlist_id']
        print(f'Uploads ID: {uploads_playlist_id}')

        playlist_response = api_get_playlist_items(uploads_playlist_id)
        playlist_items = playlist_response['items']

        if playlist_items:
            for playlist_video in playlist_items:
                snippet = playlist_video['snippet']
                try:
                    if snippet['thumbnails']['maxres']:
                        video_thumbnail = snippet['thumbnails']['maxres']['url']
                    else:
                        video_thumbnail = snippet['thumbnails']['default']['url']
                except (IndexError, KeyError):
                    video_thumbnail = 'Thumbnail-Error'

                video_upload_date = snippet['publishedAt']
                video_title = snippet['title']
                video_id = snippet['resourceId']['videoId']
                video_duration = api_get_video_duration(video_id)

                video_info = {
                    'Username': username,
                    'Video Title': video_title,
                    'Video Upload Date': video_upload_date,
                    'Video ID': video_id,
                    'Video Duration': video_duration,
                    'Video Thumbnail': video_thumbnail
                }
                all_videos.append(video_info)

                print(f'\t Video Title: \t\t {video_title}')
                print(f'\t Video Upload Date: \t {video_upload_date}')
                print(f'\t Video ID: \t\t {video_id}')
                print(f'\t Video Duration: \t {video_duration}')
                print(f'\t Video Thumbnail: \t {video_thumbnail} \n')
        else:
            return print('No videos found for {username}')

    all_videos = sorted(
        all_videos,
        key=lambda x: (x['Username'], -datetime.fromisoformat(x['Video Upload Date']).timestamp())
    )

    return all_videos

if __name__ == "__main__":
    channel_info_file_path = 'yt/data/channel_info.json'
    channel_data = get_channel_info(channel_info_file_path)

    all_videos = get_latest_videos(channel_data)

    output_path='yt/test_latest.md'
    save_to_md(all_videos, file_path=output_path)