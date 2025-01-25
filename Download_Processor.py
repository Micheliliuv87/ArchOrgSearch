import requests
import pandas as pd
import os
import re
import json

# Read the Excel file
excel_path = "rt_abortion_full_scrape.xlsx"
df = pd.read_excel(excel_path, sheet_name="Sheet1")

# Loop through each row in the Excel
for index, row in df.iterrows():
    unique_id = row['Unique Identifier']
    details_url = row['URL']  # URL to scrape the duration from
    
    # Step 1: Scrape the duration from the details page
    try:
        response = requests.get(details_url)
        html_content = response.text
        
        # Extract the JSON string containing the duration
        match = re.search(r'<input class="js-tv3-init".*?value=\'(.*?)\'/>', html_content)
        if not match:
            print(f"Skipping {unique_id}: TV3 data not found")
            continue
        
        tv3_data = json.loads(match.group(1))
        duration = float(tv3_data.get("TV3.duration", 0))
        end_time = int(duration)
        print(f"Scraped duration for {unique_id}: {end_time} seconds")
    except Exception as e:
        print(f"Error scraping {unique_id}: {str(e)}")
        continue
    
    # Step 2: Generate the base URL dynamically
    base_url = f"https://archive.org/download/{unique_id}/{unique_id}.mp4"
    
    # Step 3: Configure segment parameters
    start_time = 0
    segment_duration = 60
    save_directory = os.path.join("segments", unique_id)  # Save segments in a subfolder
    
    # Create directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    
    # Function to download segments (same as before)
    def download_segment(start, end, segment_number):
        segment_url = f"{base_url}?t={start}/{end}&ignore=x.mp4"
        filename = os.path.join(save_directory, f"segment_{segment_number}.mp4")
        response = requests.get(segment_url, stream=True)
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded {unique_id} segment {segment_number} ({start}-{end}s)")
    
    # Download all segments for this video
    segment_number = 1
    for start in range(start_time, end_time, segment_duration):
        end = start + segment_duration
        if end > end_time:
            end = end_time
        download_segment(start, end, segment_number)
        segment_number += 1

print("All videos processed.")