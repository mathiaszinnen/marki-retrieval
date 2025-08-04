import os
from PIL import Image
import matplotlib.pyplot as plt
from webservice.faiss_backend import load_faiss_index

def plot_image_dimension_histograms(images_dir, max_bins=10):
    """
    Reads all images from `images_dir` and plots two histograms:
    one for image widths, and one for image heights.
    """
    widths = []
    heights = []

    for filename in os.listdir(images_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
            path = os.path.join(images_dir, filename)
            try:
                with Image.open(path) as img:
                    width, height = img.size
                    widths.append(width)
                    heights.append(height)
            except Exception as e:
                print(f"Could not read {filename}: {e}")

    if not widths or not heights:
        print("No valid images found.")
        return

    # Plot width histogram
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.hist(widths, bins=min(max_bins, len(set(widths))), edgecolor='black')
    plt.xlabel("Width (pixels)")
    plt.ylabel("Number of Images")
    plt.title("Image Width Distribution")
    plt.grid(True)

    # Plot height histogram
    plt.subplot(1, 2, 2)
    plt.hist(heights, bins=min(max_bins, len(set(heights))), edgecolor='black')
    plt.xlabel("Height (pixels)")
    plt.ylabel("Number of Images")
    plt.title("Image Height Distribution")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    images_dir = os.path.expanduser('~/data/marki/images')
    plot_image_dimension_histograms(images_dir)