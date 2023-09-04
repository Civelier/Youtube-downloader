import re
from pytube import Playlist, YouTube
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

YOUTUBE_STREAM_ITAG = '37' # modify the value to download a different stream https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2

root = tk.Tk()
root.withdraw()


print("Select destination folder")
file_path = filedialog.askdirectory(title="Enter destination folder")


playlist_url = input("Paste playlist url here: ")

playlist = Playlist(playlist_url)

# this fixes the empty playlist.videos list
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

print(len(playlist.video_urls))
urls = []

for c, url in enumerate(playlist.video_urls):
    print(url)
    urls.append(url)

def yesno_input(prompt:str):
    while True:
        yn = input(prompt).lower()
        if yn in 'yn' and len(yn) != 0:
            return yn == 'y'
        else:
            print("Invalid answer!")

# physically downloading the audio track
print(f"Found {c} videos.")
for i, video in enumerate(urls):
    while True:
        print(f"Downloading video {i}/{c} ... ", end='')
        try:
            videoStream = YouTube(video).streams.get_highest_resolution()
        except Exception as e:
            print(e)
            videoStream = None
        if videoStream is None:
            print(f"Failed to download {video}")
            if yesno_input("Retry?"):
                continue
            else:
                break
        else: # SUCCESS
            videoStream.download(output_path=file_path)
            break
            

    print("DONE")
