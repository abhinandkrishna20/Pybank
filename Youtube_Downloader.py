from pytube import YouTube

def download_video(video_url, output_path="."):
    try:
        # Create a YouTube object with the provided URL
        youtube = YouTube(video_url)

        # Get the highest resolution stream available (mp4 format)
        video_stream = youtube.streams.get_highest_resolution()

        # Get the video title to use as the filename
        video_title = youtube.title

        # Download the video to the specified output path
        video_stream.download(output_path)

        print(f"Video '{video_title}' downloaded successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Replace 'VIDEO_URL_HERE' with the URL of the YouTube video you want to download
    print("\n\t\t Hi,\n Welcome to Youtue\t")
    video_url = input("Enter the video url: ")
    
    # Replace 'OUTPUT_PATH_HERE' with the directory where you want to save the downloaded video
    output_path = "video"
    
    download_video(video_url, output_path)
