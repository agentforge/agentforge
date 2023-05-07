import os
import sys
import subprocess
import argparse
import math


def download_video(url):
    try:
        print(f"Downloading video from '{url}'...")
        command = f"yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -o '%(title)s.%(ext)s' {url}"
        result = subprocess.run(command, shell=True, check=True)
        if result.returncode == 0:
            output = subprocess.check_output(f"yt-dlp --get-filename -o '%(title)s.%(ext)s' {url}", shell=True)
            video_filename = output.decode("utf-8").strip()
            print("Download complete.")
            return video_filename
        else:
            print("Error downloading video.")
            sys.exit(1)
    except Exception as e:
        print("Error downloading video:", e)
        sys.exit(1)


def create_output_directory(video_file):
    output_directory = os.path.splitext(video_file)[0]
    os.makedirs(output_directory, exist_ok=True)
    return output_directory

def convert_to_wav(video_file, output_directory):
    try:
        video_file = video_file.replace("webm", "mp4")
        output_file = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(video_file))[0]}.wav")
        command = f"ffmpeg -i '{video_file}' -vn -acodec pcm_s16le -ar 48000 -ac 2 '{output_file}'"
        result = subprocess.run(command, shell=True, check=True)
        if result.returncode == 0:
            print(f"Conversion complete. Output file: '{output_file}'")
        else:
            print("Error converting video to WAV.")
            sys.exit(1)
    except Exception as e:
        print("Error converting video to WAV:", e)
        sys.exit(1)

def cut_video_into_segments(video_file, n_segments, output_directory):
    try:
        video_file = video_file.replace("webm", "mp4")
        # Get video duration
        command = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '{video_file}'"
        duration = float(subprocess.check_output(command, shell=True).decode("utf-8").strip())
        segment_duration = duration / n_segments

        # Cut video into segments
        output_files = []
        for i in range(n_segments):
            start_time = i * segment_duration
            output_file = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(video_file))[0]}_segment_{i + 1}.mp4")
            command = f"ffmpeg -y -ss {start_time} -t {segment_duration} -i '{video_file}' -c copy '{output_file}'"
            result = subprocess.run(command, shell=True, check=True)
            if result.returncode == 0:
                output_files.append(output_file)
            else:
                print(f"Error cutting video segment {i + 1}.")
                sys.exit(1)

        print(f"Video has been cut into {n_segments} equal segments.")
        return output_files
    except Exception as e:
        print("Error cutting video into segments:", e)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a YouTube video and convert it to a WAV file.")
    parser.add_argument("youtube_url", help="URL of the YouTube video")
    parser.add_argument("-c", "--cuts", type=int, help="Number of equal segments to cut the video into", default=1)
    args = parser.parse_args()

    downloaded_video_file = download_video(args.youtube_url)
    output_directory = create_output_directory(downloaded_video_file)
    cut_video_files = cut_video_into_segments(downloaded_video_file, args.cuts, output_directory)

    # Convert each segment to WAV
    for video_file in cut_video_files:
        convert_to_wav(video_file, output_directory)