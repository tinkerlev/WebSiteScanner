import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

def download_file(url, folder="web.project"):
    # Attempt to send an HTTP GET request with data streaming
    response = requests.get(url, stream=True)
    # Retrieve the content type from the response headers
    content_type = response.headers.get('Content-Type')
    # Check if the content type is suitable for image or PDF files
    if 'image' in content_type or 'application/pdf' in content_type:
        # Create a local filename based on the URL
        local_filename = os.path.join(folder, url.split('/')[-1])
        # Open a file in binary write mode
        with open(local_filename, 'wb') as f:
            # Write the data to the file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {local_filename}")
    else:
        # Print a message if the file is not of the desired type
        print(f"Skipped {url}, not a target file type ({content_type}).")

def scan_website(url):
    # Create the directory if it does not exist
    if not os.path.exists('web.project'):
        os.makedirs('web.project')

    # Send a GET request to the website and parse the received content using BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search <a> tags and check the links they contain
    for link in soup.find_all('a'):
        href = link.get('href')
        # Filter out irrelevant or incorrect links
        if href and not href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
            full_url = urllib.parse.urljoin(url, href)
            print(f"Found URL: {full_url}")  # Print each URL found
            download_file(full_url, 'web.project')

    # Search <img> tags and check the links to images
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            full_img_url = urllib.parse.urljoin(url, img_url)
            print(f"Found Image URL: {full_img_url}")  # Print the image URL
            download_file(full_img_url, 'web.project')

# Call the function with an example website URL
scan_website("https://example.com")
