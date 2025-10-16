import os
import json
from utils import save_to_md, api_get_video_duration, api_get_playlist_items

def get_channel_info(channel_info_file_path):
    """Fetch the Username and Uploads Playlist ID associated."""
    print('\nRunning: get_channel_info')
    with open(channel_info_file_path, 'r') as file:
        data = json.load(file)
        # print(f'Data: {data}')
        return data
        # return data[1]

def get_latest_videos(channel_data):
    """Fetch the latest x videos from a certain playlist"""
    print('\nRunning: get_latest_videos')
    for channel in channel_data:
        username = channel['username']
        print(f'\nUsername: {username}')

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

                print(f'\t Video Title: \t\t {video_title}')
                print(f'\t Video Upload Date: \t {video_upload_date}')
                print(f'\t Video ID: \t\t {video_id}')
                print(f'\t Video Duration: \t {video_duration}')
                print(f'\t Video Thumbnail: \t {video_thumbnail} \n', flush=True)

            # return {'title': video_title, 'video_id': video_id}
        else:
            return None















# def get_latest_videos(channel_id_or_username):
#     """Fetch the latest 3 videos from the provided channel ID or username."""
#     if "youtube.com/channel/" in channel_id_or_username:
#         # If it's a channel ID, use it directly.
#         channel_id = channel_id_or_username.split("/")[-1]  # Get the last part after "/channel/"
#     elif "youtube.com/@" in channel_id_or_username:
#         # For usernames, we need to fetch the channel ID first
#         username = channel_id_or_username.split('/')[-1]  # Extract the username correctly
#         request = youtube.search().list(  # Change to search instead of channels
#             part='snippet',
#             type='channel',  # Ensure we're searching for channels
#             q=username  # Search using the username
#         )
#         response = request.execute()
        
#         # Extract the channel ID
#         if response['items']:
#             channel_id = response['items'][0]['id']['channelId']  # Get the channelId from snippet
#         else:
#             return []  # Return empty if no channel found
#     else:
#         return []  # Invalid input format

#     # Fetch the latest videos for the channel ID
#     response = youtube.search().list(
#         channelId=channel_id,
#         part='id,snippet',
#         order='date',
#         maxResults=3
#     ).execute()

#     video_list = []
#     for item in response['items']:
#         # Ensure the item is of type "video" before accessing videoId
#         if item['id']['kind'] == 'youtube#video':
#             video_list.append({
#                 'title': item['snippet']['title'],
#                 'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
#             })
#     return video_list



# def get_first_video(channel_id):
#     # # Step 1: Get the uploads playlist ID
#     # channel_request = youtube.channels().list(
#     #     part='contentDetails',
#     #     id=channel_id
#     # )
#     # channel_response = channel_request.execute()

#     uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

#     # Step 2: Get the videos from the uploads playlist
#     playlist_request = youtube.playlistItems().list(
#         part='snippet',
#         playlistId=uploads_playlist_id,
#         maxResults=1 
#     )
#     playlist_response = playlist_request.execute()

#     # Step 3: Retrieve the video details
#     if playlist_response['items']:
#         first_video = playlist_response['items'][0]['snippet']
#         video_title = first_video['title']
#         print(video_title)
#         video_id = first_video['resourceId']['videoId']
#         print(video_id)
#         return {'title': video_title, 'video_id': video_id}
#     else:
#         return None

# def scrape_videos(md_file_path):
#     """Scrape videos for both channel IDs and usernames."""
#     channel_ids = get_channel_ids(md_file_path)
#     usernames = get_usernames(md_file_path)
    
#     all_videos = {}
    
#     # Scrape videos for usernames
#     for username in usernames:
#         videos = get_latest_videos(f"https://www.youtube.com/@{username}/videos")
#         all_videos[username] = videos

#     # # Scrape videos for channel IDs
#     # for channel_id in channel_ids:
#     #     videos = get_latest_videos(f"https://www.youtube.com/channel/{channel_id}")
#     #     all_videos[channel_id] = videos
    
#     return all_videos

if __name__ == "__main__":
    channel_info_file_path = 'yt/data/channel_info.json'
    channel_data = get_channel_info(channel_info_file_path)

    get_latest_videos(channel_data)

    # Specify your Markdown file path
    # channel_ids_file = 'yt/subs.md'
    # output_path='yt/latest.md'
    # channel_ids_file = 'yt/test.md'
    # output_path='yt/test_latest.md'

    # videos = scrape_videos(channel_ids_file)
    
    # Optionally, save or format the output
    # save_to_md(videos, file_path=output_path)