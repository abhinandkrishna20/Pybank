import requests
import os
import threading

def download_chunk(url, start_byte, end_byte, filename, chunk_num, total_chunks):
    headers = {"Range": f"bytes={start_byte}-{end_byte}"}
    response = requests.get(url, headers=headers, stream=True)
    
    with open(filename, "r+b") as file:
        file.seek(start_byte)
        file.write(response.content)
    
    chunk_size = end_byte - start_byte + 1
    downloaded_bytes = chunk_size * (chunk_num + 1)  # Add 1 to include the current chunk
    total_size = os.path.getsize(filename)

    # Calculate progress and print
    progress = (downloaded_bytes / total_size) * 100
    print(f"Chunk {chunk_num + 1}/{total_chunks} - {progress:.2f}% downloaded")

def download_file(url, num_chunks=16, destination_folder="."):
    try:
        # Send a HEAD request to get the total file size
        response = requests.head(url)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        # Calculate the chunk size and ranges
        chunk_size = total_size // num_chunks
        ranges = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_chunks - 1)]
        ranges.append((ranges[-1][1] + 1, total_size - 1))

        # Create a file with the same name as the URL's filename in the destination folder
        filename = os.path.join(destination_folder, os.path.basename(url))
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

if __name__ == "__main__":
    url = input("Enter the URL of the file to download: ")
    download_file(url, num_chunks=16)
