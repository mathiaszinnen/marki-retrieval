import requests
import csv
import os
import re


def get_marks_page(base_url, number):
    """
    Retrieve the n-th page of marks for further processing. """
    page_url = f'{base_url}/rest/marks?id=all&page={str(number)}'
    response = requests.get(page_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Request failed for {number}: {page_url}')
        return None

def extract_artist(assignment_string):
    """Extract artist from ArtistAssignment string assuming that it is the only expression in brackets."""
    matches = re.findall(r'\(([^)]+)\)', assignment_string)
    if len(matches) != 1:
        raise ValueError("None or multiple bracketed expressions found.")
    return matches[0].strip()

def has_valid_image(entry):
    if not 'Image' in entry:
        return False
    image_exts = ['.jpg', '.jpeg', '.bmp', '.tiff']
    if not any(entry['Image'].casefold().endswith(ext) for ext in image_exts):
        return False
    return True

def download_image(rel_image_path, base_url, target_dir):
    image_url = f'{base_url}/{rel_image_path}'
    image_filename = os.path.basename(image_url)

    target_path = os.path.join(target_dir, image_filename)
    if os.path.exists(target_path):
        print(f"Image already exists: {target_path}")
        return
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {target_path}")
    else:
        print(f"Failed to download {image_url} (Status code: {response.status_code})")

    return image_filename


def process_page(page_json, base_url, target_dir, writer):
    for entry in page_json:
        if not has_valid_image(entry):
            continue # skip entries without image
        try:
            artist = extract_artist(entry['ArtistAssignment'])
        except ValueError:
            artist = '' # no artist or multiple options found -> leave empty
        image_paths = [p.strip() for p in entry['Image'].split(',')]
        for rel_image_path in image_paths:
            image_filename = download_image(rel_image_path, base_url, target_dir)
            writer.writerow({'filename': image_filename, 'artist': artist}) # todo: sometimes images appear twice. Check if one image can have multiple artists (should not?!)
        
        
def download_all(base_url, target_dir):
    """
    Loop through all available pages and download images and metadata.
    Stops when an empty page is returned.
    """
    os.makedirs(target_dir, exist_ok=True)
    csv_path = os.path.join(target_dir, 'labels.csv')
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'artist'])
        writer.writeheader()
        page_num = 0
        while True:
            print(f"\nFetching page {page_num}...")
            page_json = get_marks_page(base_url, page_num)
            if not page_json:
                print(f"No more entries found on page {page_num}. Stopping.")
                break
            process_page(page_json, base_url, target_dir, writer)
            page_num += 1


if __name__ == '__main__':
    base_url = 'https://ngk.wisski.cloud'
    target_dir = os.path.expanduser('~/data/marki')
    download_all(base_url, target_dir)