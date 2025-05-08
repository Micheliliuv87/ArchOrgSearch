import glob
import os
import re
import json
import requests
import pandas as pd

# 1) Find all your Excel outputs in the working directory
excel_paths = glob.glob("meta_data/*_abortion.xlsx")

def scrape_duration(details_url, unique_id):
    """Fetch the details page and extract duration in seconds."""
    try:
        resp = requests.get(details_url)
        resp.raise_for_status()
        html = resp.text
        m = re.search(r"<input class=\"js-tv3-init\".*?value='(.*?)'/>", html)
        if not m:
            print(f"[{unique_id}] ▶ TV3 data not found, skipping.")
            return None
        data = json.loads(m.group(1))
        return int(float(data.get("TV3.duration", 0)))
    except Exception as e:
        print(f"[{unique_id}] ✖ Error scraping duration: {e}")
        return None

def download_segments(unique_id, duration, creator):
    """Download 60-second segments of the mp4 into segments/<creator>/<unique_id>/"""
    base_url = f"https://archive.org/download/{unique_id}/{unique_id}.mp4"
    save_root = os.path.join("segments", creator, unique_id)
    os.makedirs(save_root, exist_ok=True)

    segment_length = 60
    segment_num = 1
    for start in range(0, duration, segment_length):
        end = min(start + segment_length, duration)
        seg_url = f"{base_url}?t={start}/{end}&ignore=x.mp4"
        out_path = os.path.join(save_root, f"segment_{segment_num}.mp4")
        try:
            with requests.get(seg_url, stream=True) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
            print(f"[{unique_id}] ✔ Downloaded segment {segment_num} ({start}-{end}s)")
        except Exception as e:
            print(f"[{unique_id}] ✖ Failed segment {segment_num}: {e}")
        segment_num += 1

# 2) Loop over each Excel file
for excel_path in excel_paths:
    creator = os.path.basename(excel_path).split("_")[0]
    print(f"\n=== Processing creator: {creator} (file: {excel_path}) ===")
    df = pd.read_excel(excel_path)

    for _, row in df.iterrows():
        uid = row["Unique Identifier"]
        url = row["URL"]

        # 3) Scrape duration
        dur = scrape_duration(url, uid)
        if dur is None or dur == 0:
            continue

        # 4) Download segments
        download_segments(uid, dur, creator)

print("\nAll files processed.")
