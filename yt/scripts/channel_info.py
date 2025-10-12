import json
import requests
import os

def get_usernames_from_md(md_file_path):
    """Extract usernames from the specified Markdown file."""
    usernames = []
    
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
                    username = url.split('/')[-2]  # Get the part before '/videos' for username
                    usernames.append(username)

    return usernames

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
        print(f'{username} \n {data} \n\n')
        if data.get('items'):
            channel_id = resp_data['items'][0]['id']
            print(f'Channel id: {channel_id}')

            uploads_playlist_id = resp_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            print(f'Uploads id: {uploads_playlist_id}')

            return channel_id, uploads_playlist_id
    
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
    usernames = get_usernames_from_md(md_file_path)
    existing_data = load_existing_data(output_file)

    # Create a dictionary for fast lookup of existing usernames and their IDs
    existing_dict = {
        entry['username']: (entry['channel_id'], entry.get('uploads_playlist_id')) for entry in existing_data
    }

    channel_ids = []

    for username in usernames:
        channel_id, uploads_playlist_id = existing_dict.get(username, (None, None))  # Check if we already have the ID and playlist ID

        # Fetch info if either channel_id or uploads_playlist_id is missing
        if not channel_id or not uploads_playlist_id:
            channel_id, uploads_playlist_id = fetch_channel_info(username)

        # Prepare the updated channel entry
        channel_entry = {
            'username': username,
            'channel_id': channel_id,
            'uploads_playlist_id': uploads_playlist_id
        }
        channel_ids.append(channel_entry)

    # Remove duplicates in channel_ids based on username
    unique_channel_ids = {entry['username']: entry for entry in channel_ids}.values()

    # Update existing records in existing_data or add new ones
    for entry in existing_data:
        for channel in unique_channel_ids:
            if entry['username'] == channel['username']:
                entry['channel_id'] = channel['channel_id']
                entry['uploads_playlist_id'] = channel['uploads_playlist_id']
                break
        else:
            # If username wasn't found, append a new entry
            existing_data.append(channel)

    # Update the output file with the new user data
    update_channel_ids(output_file, list(existing_data))

if __name__ == "__main__":
    # md_file_path = 'yt/subs.md'
    md_file_path = 'yt/test.md'
    output_file = 'yt/data/channel_info.json'
    main(md_file_path, output_file)
