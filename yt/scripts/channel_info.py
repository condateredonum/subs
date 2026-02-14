import json
import requests
import os

def get_usernames_from_md(md_file_path):
    """Extract usernames and channel IDs from the specified Markdown file."""
    channels = []
    
    with open(md_file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace
            
            # Skip empty lines
            if not line:
                continue
            
            if "](" in line:
                url = line.split('](')[-1].strip(')')
                
                # Format: https://www.youtube.com/@Channel/videos
                if "youtube.com/@" in url:
                    username = url.split('/')[3]
                    if username.lower() not in [c['identifier'].lower() for c in channels if c['type'] == 'username']:
                        channels.append({'type': 'username', 'identifier': username})
                
                # Format: https://www.youtube.com/channel/CHANNEL_ID
                elif "youtube.com/channel/" in url:
                    channel_id = url.split('/channel/')[-1].split('/')[0]
                    if channel_id.lower() not in [c['identifier'].lower() for c in channels if c['type'] == 'channel_id']:
                        channels.append({'type': 'channel_id', 'identifier': channel_id})
    
    return channels

def fetch_channel_info(username):
    """Fetch the channel ID for a given username from YouTube."""
    api_key = os.environ.get('YOUTUBE_API_KEY')
    base_url = f'https://www.googleapis.com/youtube/v3/channels?'
    
    # Request to get channel details
    params = {
        'part': 'contentDetails',
        'forHandle': username,
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('items'):
            channel_id = data['items'][0]['id']
            print(f'Channel id: {channel_id}')
            uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            print(f'Uploads id: {uploads_playlist_id}')
            return channel_id, uploads_playlist_id
    
    return None

def fetch_channel_info_by_id(channel_id):
    """Fetch the channel info for a given channel ID from YouTube."""
    api_key = os.environ.get('YOUTUBE_API_KEY')
    base_url = f'https://www.googleapis.com/youtube/v3/channels?'
    
    # Request to get channel details
    params = {
        'part': 'contentDetails,snippet',
        'id': channel_id,
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('items'):
            channel_id = data['items'][0]['id']
            print(f'Channel id: {channel_id}')
            uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            print(f'Uploads id: {uploads_playlist_id}')
            # Try to get the custom URL/handle if available
            custom_url = data['items'][0]['snippet'].get('customUrl', '')
            username = custom_url.lstrip('@') if custom_url.startswith('@') else ''
            return channel_id, uploads_playlist_id, username
    
    return None

def load_existing_data(output_file):
    """Load existing usernames and channel IDs from JSON file."""
    if os.path.exists(output_file):
        with open(output_file, 'r') as json_file:
            try:
                channel_ids = json.load(json_file)
            except json.JSONDecodeError:
                channel_ids = []
        return channel_ids

def update_channel_ids(output_file, channel_ids):
    """Update user data in the JSON output file."""
    with open(output_file, 'w') as json_file:
        json.dump(channel_ids, json_file, indent=4)

def main(md_file_path, output_file):
    """Main function to manage the workflow."""
    channels = get_usernames_from_md(md_file_path)
    existing_data = load_existing_data(output_file)
    
    # Create a dictionary for fast lookup of existing channels by both username and channel_id
    existing_dict = {}
    for entry in existing_data:
        if entry.get('username'):
            existing_dict[('username', entry['username'])] = entry
        if entry.get('channel_id'):
            existing_dict[('channel_id', entry['channel_id'])] = entry
    
    channel_ids = []
    processed_identifiers = set()
    
    for channel in channels:
        identifier = channel['identifier']
        channel_type = channel['type']
        
        print(f'\n\tTry: {identifier} (type: {channel_type})')
        
        try:
            # Check if we already have data for this channel
            existing_entry = existing_dict.get((channel_type, identifier))
            
            if existing_entry and existing_entry.get('channel_id') and existing_entry.get('uploads_playlist_id'):
                # Use existing data
                channel_id = existing_entry['channel_id']
                uploads_playlist_id = existing_entry['uploads_playlist_id']
                username = existing_entry.get('username', '')
            else:
                # Fetch new data
                if channel_type == 'username':
                    result = fetch_channel_info(identifier)
                    if result:
                        channel_id, uploads_playlist_id = result
                        username = identifier
                    else:
                        print(f'Failed to retrieve info for username: {identifier}')
                        continue
                else:  # channel_id
                    result = fetch_channel_info_by_id(identifier)
                    if result:
                        channel_id, uploads_playlist_id, username = result
                    else:
                        print(f'Failed to retrieve info for channel ID: {identifier}')
                        continue
            
            # Avoid duplicates based on channel_id
            if channel_id not in processed_identifiers:
                channel_entry = {
                    'username': username,
                    'channel_id': channel_id,
                    'uploads_playlist_id': uploads_playlist_id
                }
                channel_ids.append(channel_entry)
                processed_identifiers.add(channel_id)
            
        except Exception as e:
            print(f'Failed to retrieve {identifier}: {e}')
            continue
    
    # Remove existing entries for the channels being updated (by channel_id)
    existing_data = [entry for entry in existing_data if entry.get('channel_id') not in processed_identifiers]
    
    # Add updated channel entries to existing_data
    existing_data.extend(channel_ids)
    
    # Update the output file with the new user data
    update_channel_ids(output_file, list(existing_data))

if __name__ == "__main__":
    md_file_path = 'yt/subs.md'
    # md_file_path = 'yt/test.md'
    output_file = 'yt/data/channel_info.json'
    main(md_file_path, output_file)