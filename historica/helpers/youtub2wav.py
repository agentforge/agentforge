import os
import sys
from pytube import YouTube
from moviepy.editor import *

def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension="mp4").first()
        print(f"Downloading '{yt.title}'...")
        video.download()
        print("Download complete.")
        return video.default_filename
    except Exception as e:
        print("Error downloading video:", e)
        sys.exit(1)


def convert_to_wav(video_file):
    try:
        output_file = os.path.splitext(video_file)[0] + ".wav"
        video = VideoFileClip(video_file)
        print(f"Converting '{video_file}' to WAV...")
        video.audio.write_audiofile(output_file, codec="pcm_s16le", nbytes=2, bitrate="48k")
        print(f"Conversion complete. Output file: '{output_file}'")
    except Exception as e:
        print("Error converting video to WAV:", e)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <youtube_url>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    downloaded_video_file = download_video(youtube_url)
    convert_to_wav(downloaded_video_file)
