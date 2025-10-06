# yt/scripts/channel_ids.py

def get_channel_ids(md_file_path):
    """Extract channel IDs from the specified Markdown file."""
    channel_ids = []
    
    with open(md_file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace
            
            # Skip empty lines
            if not line:
                continue
            
            if "](" in line:
                url = line.split('](')[-1].strip(')')
                
                # Format: https://www.youtube.com/channel/CHANNEL_ID
                if "youtube.com/channel/" in url:
                    channel_id = url.split('/')[-1]  # Get the last part for channel ID
                    channel_ids.append(channel_id)

    return channel_ids

def get_usernames(md_file_path):
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
