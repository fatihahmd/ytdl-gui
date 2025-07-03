import subprocess
import json
import time
import sys
import re

def byte_handler(num):
    if num > 999999999:
        num = num / 1000000000
        return str(f"{num:.2f}") + "GB"
    elif num > 999999:
        num = num / 1000000
        return str(f"{num:.2f}") + "MB"
    elif num > 999:
        num = num / 1000
        return str(f"{num:.2f}") + "KB"
    else:
        return str(f"{num:.2f}") + "B"
    
def format_filter(format):
    if format.get('filesize') != None:
        if "drc" not in format['format_id']:
            if "none" not in format.get('vcodec'):
                # video filtering
                if format.get('height') >= (480): # resolution more than 480p
                    if "vp9" not in format.get('vcodec'): # remove vp9 for compatibility 
                        return format
            else:
                # audio filtering
                if "opus" not in format.get('acodec'):
                    return format
    
url_pattern = re.compile('^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$')
while True:
    url = input("YouTube link: ")
    if url_pattern.match(url):
        break
    print("Error: Please use the correct YouTube link")

cmd = ["yt-dlp.exe", "-J", url]
res = subprocess.run(cmd, capture_output=True, text=True, shell=True)

data = json.loads(res.stdout)
title = data.get("title", "Unknown Title")
formats = data.get("formats", [])

filtered_formats = [fmt for fmt in formats if format_filter(fmt)]
filtered_formats.reverse()
filtered_formats_dict = {i: fmt['format_id'] for i, fmt in enumerate(filtered_formats)}

for i, fmt in enumerate(filtered_formats):
    print(f"ID: {fmt['format_id']}, Resolution: {fmt.get('resolution', 'N/A')}, Codec: {fmt.get('vcodec', 'N/A')} + {fmt.get('acodec', 'N/A')}, Size: {fmt.get('filesize', 'Unknown')}")
    # print(f"{i} - Resolution: {fmt.get('resolution', 'N/A')}, Size: {byte_handler(fmt.get('filesize'))}")

select = int(input(f"Select your option (0 - {len(filtered_formats)-1}): "))

format_id =  filtered_formats_dict[select]
    
if filtered_formats[select].get("acodec") == 'none': # if video has no audio then merge with best audio
    cmd = f"yt-dlp.exe -P \"output\" -f \"{format_id}+ba/b\" {url} --merge-output-format \"mp4\""
else: # for audio only
    cmd = f"yt-dlp.exe -P \"output\" -f \"{format_id}\" -x --audio-format mp3 {url}"

subprocess.Popen(cmd)