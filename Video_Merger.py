from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(video_paths, output_path):
    clips = [VideoFileClip(path) for path in video_paths]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, codec="libx264")
    for clip in clips:
        clip.close()

if __name__ == "__main__":
    # Provide the paths of the videos you want to merge
    video_paths = ["1.mp4", "2.mp4", "3.mp4","4.mp4"]

    # Provide the output path for the merged video
    output_path = "merged_video.mp4"

    merge_videos(video_paths, output_path)
