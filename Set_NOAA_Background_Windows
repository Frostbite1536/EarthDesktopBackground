import os
import ctypes
import requests
import pathlib
import sys
import time

# --- Configuration ---
NOAA_IMAGE_URL = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/FD/GEOCOLOR/latest.jpg"
# Use Local AppData for storing the image - creates folder if it doesn't exist
SAVE_DIR = pathlib.Path(os.getenv('LOCALAPPDATA', '')) / "NOAA_Wallpaper"
SAVE_FILENAME = "noaa_latest_background.jpg"
IMAGE_PATH = SAVE_DIR / SAVE_FILENAME

# --- Windows API Constants ---
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 1
SPIF_SENDWININICHANGE = 2

# --- Functions ---

def download_image(url, save_path):
    """Downloads an image from the URL and saves it to the specified path."""
    print(f"-> Attempting to download image from: {url}")
    try:
        # Ensure the save directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Make the request with a timeout and stream=True for potentially large files
        response = requests.get(url, stream=True, timeout=30) # 30-second timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Save the image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"-> Image successfully downloaded and saved to: {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"!! Error downloading image: {e}", file=sys.stderr)
        return False
    except OSError as e:
        print(f"!! Error saving image file: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"!! An unexpected error occurred during download: {e}", file=sys.stderr)
        return False

def set_windows_background(image_path):
    """Sets the Windows desktop background to the specified image file."""
    print(f"-> Attempting to set background to: {image_path}")
    # Ensure the path is absolute and exists
    abs_image_path = str(image_path.resolve())
    if not image_path.is_file():
        print(f"!! Error: Image file not found at {abs_image_path}", file=sys.stderr)
        return False

    try:
        # Use SystemParametersInfoW for Unicode path support
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            abs_image_path,
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
        )
        if result:
            print("-> Desktop background updated successfully.")
            return True
        else:
            # You might need error checking here using GetLastError if it fails
            print("!! Error: Failed to set desktop background via SystemParametersInfoW.", file=sys.stderr)
            # Attempting to get more error info (may require admin rights for some errors)
            error_code = ctypes.windll.kernel32.GetLastError()
            print(f"!! Windows API error code: {error_code}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"!! An unexpected error occurred while setting background: {e}", file=sys.stderr)
        return False

# --- Main Execution ---

if __name__ == "__main__":
    print("--- NOAA GOES-19 Background Setter ---")

    if download_image(NOAA_IMAGE_URL, IMAGE_PATH):
        # Brief pause to ensure file is fully written and accessible
        time.sleep(1)
        set_windows_background(IMAGE_PATH)
    else:
        print("!! Background not updated due to download failure.")

    print("--- Script finished ---")
    # Optional: Keep console open for a few seconds to see output
    # time.sleep(5)
