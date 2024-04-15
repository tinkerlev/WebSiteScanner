import requests
from bs4 import BeautifulSoup
import os
import urllib.request

def scan_website(url):
    # Create a directory named 'web.project' if it does not already exist
    if not os.path.exists('web.project'):
        os.makedirs('web.project')

    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize an empty set to store unique paths
    paths = set()
    # Find all 'a' tags (which define hyperlinks) in the HTML
    for link in soup.find_all('a'):
        href = link.get('href')
        # Check if href attribute exists and does not start with mailto:, tel:, or javascript:
        if href and not href.startswith(('mailto:', 'tel:', 'javascript:')):
            print("Path found:", href)
            paths.add(href)

    # Iterate over each path found on the page
    for path in paths:
        # Check if the path ends with .pdf, .jpg, .jpeg, or .png
        if path.endswith('.pdf') or any(path.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            # Construct the full URL to the file
            full_path = urllib.parse.urljoin(url, path)
            # Define the file name by combining the directory name and the base name of the path
            file_name = os.path.join('web.project', os.path.basename(full_path))
            try:
                # Attempt to download the file to the specified location
                urllib.request.urlretrieve(full_path, file_name)
                print(f"Downloaded {file_name}")
            except Exception as e:
                # Print an error message if the download fails
                print(f"Failed to download {full_path}: {e}")

# Example usage: replace "https://example.com" with the URL of the site you wish to scan
scan_website("https://example.com")
