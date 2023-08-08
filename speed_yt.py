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

def calculate_ranges(total_size, num_chunks):
    # Calculate the ranges of bytes that will be downloaded for each chunk
    ranges = []
    chunk_size = total_size // num_chunks
    for i in range(num_chunks - 1):
        ranges.append((i * chunk_size, (i + 1) * chunk_size - 1))
    # Add the last chunk
    ranges.append((ranges[-1][1] + 1, total_size - 1))
    return ranges

def download_chunk(url, start_byte, end_byte, filename, chunk_num, total_chunks):
    headers = {"Range": f"bytes={start_byte}-{end_byte}"}
    response = requests.get(url, headers=headers, stream=True)

    with open(filename, "r+b") as file:
        file.seek(start_byte)
        file.write(response.content)

    chunk_size = end_byte - start_byte + 1
    downloaded_bytes = chunk_size * (chunk_num + 1)  # Add 1 to include the current chunk

    # Calculate progress and update the progress bar
    progress = (downloaded_bytes / total_size) * 100
    tqdm.write(f"Chunk {chunk_num + 1}/{total_chunks} - {progress:.2f}% downloaded", end="")

def download_file(url, output_path=".", num_chunks=16):
    try:
        filename = os.path.basename(url)

        # Get the total size of the file
        total_size = int(requests.head(url).headers.get("content-length", 0))

        # Calculate the ranges of bytes that will be downloaded for each chunk
        ranges = calculate_ranges(total_size, num_chunks)

        # Create an empty file with the sanitized filename in the output path
        with open(filename, "wb") as file:
            file.truncate(total_size)

        # Start download threads for each chunk
        threads = []
        for i, (start_byte, end_byte) in enumerate(ranges):
            thread = threading.Thread(
                target=download_chunk,
                args=(url, start_byte, end_byte, filename, i, num_chunks)
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
    print("\n\t\t Hi,\n Welcome to File Downloader\t")
    file_url = input("\n\nPlease give the link :- ")

    # Set the output_path to the current directory (the directory where the script is located)
    output_path = "."

 
