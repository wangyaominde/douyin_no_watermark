import requests
import re
import sys
import os
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_real_url(share_text):
    # Extract URL using regex
    url_pattern = re.compile(r'https?://v\.douyin\.com/[a-zA-Z0-9]+/')
    match = url_pattern.search(share_text)
    if not match:
        print("No Douyin URL found in text")
        return None
    return match.group(0)

def download_video(share_text):
    short_url = get_real_url(share_text)
    if not short_url:
        return

    print(f"Analyzing URL: {short_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }
    
    try:
        session = requests.Session()
        session.headers.update(headers)
        
        # 1. Follow redirect to get long URL
        response = session.get(short_url, allow_redirects=False, verify=False)
        if response.status_code not in [301, 302]:
            print(f"Failed to retrieve long URL. Status: {response.status_code}")
            return

        long_url = response.headers['Location']
        print(f"Redirected to: {long_url}")
        
        # 2. Fetch page content to find video_id
        page_resp = session.get(long_url, verify=False)
        
        # Extract video_id from playwm URL
        vid_pattern = re.compile(r'video_id=([a-zA-Z0-9]+)')
        match = vid_pattern.search(page_resp.text)
        
        if not match:
            print("Could not find video ID in page content.")
            return

        video_id = match.group(1)
        print(f"Found Video ID: {video_id}")
        
        # 3. Construct API URL for no-watermark video
        # Using api.amemv.com as it seems more reliable for this
        # Use 1080p for higher quality
        api_url = f"https://api.amemv.com/aweme/v1/play/?video_id={video_id}&ratio=1080p&line=0"
        
        # 4. Get the real video location
        play_resp = session.get(api_url, allow_redirects=False, verify=False)
        
        if play_resp.status_code not in [301, 302]:
            print(f"Failed to get video location. Status: {play_resp.status_code}")
            return
            
        real_video_url = play_resp.headers['Location']
        print(f"Downloading from: {real_video_url}")
        
        # 5. Download the video
        video_resp = session.get(real_video_url, verify=False, stream=True)
        
        # Setup output directory
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Extract filename from headers or generate one
        filename = os.path.join(output_dir, f"douyin_{video_id}.mp4")
        
        total_size = int(video_resp.headers.get('content-length', 0))
        block_size = 1024 # 1 Kibibyte
        
        with open(filename, 'wb') as f:
            downloaded = 0
            for data in video_resp.iter_content(block_size):
                downloaded += len(data)
                f.write(data)
                # Simple progress bar
                if total_size > 0:
                    percent = int(50 * downloaded / total_size)
                    sys.stdout.write(f"\r[{'=' * percent}{' ' * (50 - percent)}] {downloaded}/{total_size} bytes")
                    sys.stdout.flush()
        
        print(f"\nVideo saved to: {os.path.abspath(filename)}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = input("Please enter the Douyin share text or URL: ")
    
    download_video(text)

