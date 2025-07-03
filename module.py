import subprocess
import json
import re
import yt_dlp

progress_callback = None

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
    
def _format_filter(formats):
    return list(reversed([
        format for format in formats 
        if format.get('filesize') is not None 
        and 'drc' not in format['format_id'] 
        and (('none' not in format.get('vcodec')
            #   video formats
             and format.get('height') >= (480) 
             and "vp9" not in format.get('vcodec')) 
            #  audio formats
             or ('none' in format.get('vcodec') 
                 and "opus" not in format.get('acodec'))
             )]))

def _progress_hook(d):
    if d['status'] == 'downloading' and progress_callback:
        progress = float(d['downloaded_bytes']/d['total_bytes']*100)
        speed = d['speed']
        progress_callback(progress, speed)

def download_yt(format_id, url, callback_funct=None):
    global progress_callback
    progress_callback = callback_funct
    with yt_dlp.YoutubeDL({'format': format_id, 'progress_hooks': [_progress_hook]}) as ytdl:
        ytdl.download([url])

def get_formats(url_input):
    url_pattern = re.compile('^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$')
    while True:
        url = url_input
        if url_pattern.match(url):
            break
        print("Error: Please use the correct YouTube link")

    with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ytdl:
        data = ytdl.extract_info(url_input, download=False)
    
    formats = data.get("formats", [])
    title = data.get("title", "Unknown Title")

    return _format_filter(formats), title


def get_formats_legacy(url_input): # uses yt-dlp.exe files, not the library
    url_pattern = re.compile('^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$')
    while True:
        url = url_input
        if url_pattern.match(url):
            break
        print("Error: Please use the correct YouTube link")

    cmd = ["yt-dlp.exe", "-J", url]
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)

    data = json.loads(res.stdout)
    # title = data.get("title", "Unknown Title")
    formats = data.get("formats", [])

    return _format_filter(formats)
    # filtered_formats_dict = {i: fmt['format_id'] for i, fmt in enumerate(filtered_formats)}

    # for i, fmt in enumerate(filtered_formats):
    #     print(f"ID: {fmt['format_id']}, Resolution: {fmt.get('resolution', 'N/A')}, Codec: {fmt.get('vcodec', 'N/A')} + {fmt.get('acodec', 'N/A')}, Size: {fmt.get('filesize', 'Unknown')}")
    #     # print(f"{i} - Resolution: {fmt.get('resolution', 'N/A')}, Size: {byte_handler(fmt.get('filesize'))}")

    # select = int(input(f"Select your option (0 - {len(filtered_formats)-1}): "))

    # format_id =  filtered_formats_dict[select]
        
    # if filtered_formats[select].get("acodec") == 'none': # if video has no audio then merge with best audio
    #     cmd = f"yt-dlp.exe -P \"output\" -f \"{format_id}+ba/b\" {url} --merge-output-format \"mp4\""
    # else: # for audio only
    #     cmd = f"yt-dlp.exe -P \"output\" -f \"{format_id}\" -x --audio-format mp3 {url}"

    # subprocess.Popen(cmd)
__all__ = ["get_formats"]  