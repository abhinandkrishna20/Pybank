import requests
import os
import threading
from pytube import YouTube
from tqdm import tqdm
import re

def sanitize_filename(title):
    # Remove any characters that are not allowed in filenames
    # Replace them with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', title)

def download_chunk(url, start_byte, end_byte, filename, chunk_num, total_chunks):
    headers = {"Range": f"bytes={start_byte}-{end_byte}"}
    response = requests.get(url, headers=headers, stream=True)

    with open(filename, "r+b") as file:
        file.seek(start_byte)
        file.write(response.content)

    chunk_size = end_byte - start_byte + 1
    downloaded_bytes = chunk_size * (chunk_num + 1)  # Add 1 to include the current chunk
    total_size = os.path.getsize(filename)

    # Calculate progress and update the progress bar
    progress = (downloaded_bytes / total_size) * 100
    tqdm.write(f"Chunk {chunk_num + 1}/{total_chunks} - {progress:.2f}% downloaded", end="")

def download_video(video_url, output_path=".", num_chunks=16):
    try:
        # Create a YouTube object with the provided URL
        youtube = YouTube(video_url)

        # Get the highest resolution stream available (mp4 format)
        video_stream = youtube.streams.get_highest_resolution()

        # Get the video title and sanitize it to use as the filename
        video_title = sanitize_filename(youtube.title)

        # Prepare the filename and the full path
        filename = os.path.join(output_path, f"{video_title}.mp4")

        # Send a HEAD request to get the total file size
        response = requests.head(video_stream.url)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        # Calculate the chunk size and ranges
        chunk_size = total_size // num_chunks
        ranges = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_chunks - 1)]
        ranges.append((ranges[-1][1] + 1, total_size - 1))

        # Create an empty file with the sanitized filename in the output path
        with open(filename, "wb") as file:
            file.truncate(total_size)

        # Start download threads for each chunk
        threads = []
        for i, (start_byte, end_byte) in enumerate(ranges):
            thread = threading.Thread(
                target=download_chunk,
                args=(video_stream.url, start_byte, end_byte, filename, i, num_chunks)
            )
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print("\nDownload completed!")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("\n\t\t Hi,\n Welcome to YouTube Downloader\t")
    video_url = input("Enter the video url: ")

    # Set the output_path to the current directory (the directory where the script is located)
    output_path = "."

    # Specify the desired number of chunks to use for concurrent downloading
    num_chunks = 32  # For example, you can set it to 8 or any other appropriate value.

    download_video(video_url, output_path, num_chunks)
