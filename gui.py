import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from module import get_formats, byte_handler
from module import download_yt
import re

window = tk.Tk()
# window.configure(bg="white")
window.geometry("400x300")
window.resizable(False,False)
window.title("YT Downloader GUI")

URL = tk.StringVar()
SELECTED_OPT = tk.StringVar()

def update_progress(value, speed):
        progress1['value'] = value
        if value == 100:
            status1.config(text="Success!")
            showinfo(title="Notice", message="Download Success")
        else:
            speed = speed/1000
            status1.config(text=f"{speed:.2f} KB/s") 
        window.update_idletasks()

# calls yt-dlp to download specific format id
def format_download(URL_current):
    progress1["value"] = 0
    download_yt(SELECTED_OPT.get(), URL_current, update_progress)
    # showinfo(title='NOTICE', message=f'url: {URL_current} selected id: {SELECTED_OPT.get()}')
    

# gets format options
def get_format_list():
    URL_current = URL.get()
    formats, title = get_formats(URL_current)

    for widget in result_frame.winfo_children():
        widget.destroy()
    
    title1 = ttk.Label(text=f'Title: {title}', wraplength=300, justify='center')
    title1.pack(padx=10)

    for x in formats:
        rb = ttk.Radiobutton(result_frame, text=f"Res: {x.get('resolution')}, Size: {byte_handler(x.get('filesize'))}", variable=SELECTED_OPT, value=x['format_id'])
        rb.pack(anchor='w', padx=10)
        
    # result_frame.pack(fill="x")
    
    b = ttk.Button(result_frame, text="Download Format", command=lambda: format_download(URL_current))
    b.pack(anchor='w', padx=10)

# validate youtube url
url_pattern = re.compile('^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$')
def validate_url(*args):
    if re.match(url_pattern, URL.get().strip()):
        button1.config(state='enabled')
    else:
        button1.config(state='disabled')     
URL.trace_add('write', validate_url)

# containers
input_frame = ttk.Frame(window)
input_frame.pack(padx=10, fill="x", expand=True)

result_frame = ttk.Frame(window)
result_frame.pack(padx=10, fill="x", expand=True)

progress_frame = ttk.Frame(window)
progress_frame.pack(padx=10, fill="x", expand=True)


# widgets
label1 = ttk.Label(input_frame, text="Insert YouTube URL:")
label1.pack(side="top", padx=10, fill="x", expand=True)

entry1 = ttk.Entry(input_frame, textvariable=URL)
entry1.pack(side="left", padx=10, fill="x", expand=True)

button1 = ttk.Button(input_frame, text="Find Video", command=get_format_list, state='disabled')
button1.pack(side="left", padx=10, fill="x")

status1 = ttk.Label(progress_frame, text="Ready to Download")
status1.pack(padx=10)
progress1 = ttk.Progressbar(progress_frame, orient='horizontal', length=300, mode="determinate")
progress1.pack(padx=10)

window.mainloop()