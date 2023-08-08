import requests
import os

def download_file(url, destination_folder="."):
    try:
        # Get the filename from the URL
        filename = os.path.join(destination_folder, os.path.basename(url))
        
        # Send an HTTP request to get the file stream
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get the total file size (if provided by the server)
        total_size = int(response.headers.get("content-length", 0))
        
        # Open the local file for writing
        with open(filename, "wb") as file:
            chunk_size = 1024  # 1 KB
            downloaded_size = 0
            
            # Iterate over the file content and save it in chunks
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                downloaded_size += len(chunk)
                
                # Calculate and display the download progress
                progress = (downloaded_size / total_size) * 100
                print(f"Downloaded {downloaded_size} / {total_size} bytes ({progress:.2f}%)", end="\r")
        
        print("\nDownload completed!")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url = input("Enter the URL of the file to download: ")
    download_file(url)
