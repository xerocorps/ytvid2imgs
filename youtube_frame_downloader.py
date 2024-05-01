import os
import sys
import argparse
from pytube import YouTube
from moviepy.editor import VideoFileClip

def download_video(url, output_dir):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        video.download(output_dir)
        return True, os.path.join(output_dir, video.default_filename)
    except Exception as e:
        return False, str(e)

def extract_frames(video_path, output_dir, frame_interval):
    try:
        clip = VideoFileClip(video_path)
        fps = clip.fps
        frame_count = int(clip.duration * fps)
        for i in range(0, frame_count, frame_interval):
            frame_path = os.path.join(output_dir, f"{i}.png")
            clip.save_frame(frame_path, t=i/fps)
        return True
    except Exception as e:
        return False, str(e)

def main(url, output_dir, frame_interval):
    success, video_path = download_video(url, output_dir)
    if not success:
        print("Failed to download video:", video_path)
        sys.exit(1)
    
    print("Video downloaded successfully:", video_path)
    
    success = extract_frames(video_path, output_dir, frame_interval)
    if not success:
        print("Failed to extract frames from the video.")
        sys.exit(1)
    
    print("Frames extracted successfully and saved to:", output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video frame-wise and save to a directory by timestamps")
    parser.add_argument("url", type=str, help="YouTube video URL")
    parser.add_argument("-o", "--output", type=str, default="frames", help="Output directory to save frames (default: frames)")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Frame extraction interval in seconds (default: 10)")
    args = parser.parse_args()
    
    main(args.url, args.output, args.interval)
