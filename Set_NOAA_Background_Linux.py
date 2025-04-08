#!/usr/bin/env python3

import os
import requests
import pathlib
import sys
import time
import subprocess
import shutil

# --- Configuration ---
NOAA_IMAGE_URL = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/FD/GEOCOLOR/latest.jpg"
# Use a cache directory in the user's home directory
SAVE_DIR = pathlib.Path.home() / ".cache" / "noaa_wallpaper"
SAVE_FILENAME = "noaa_latest_background.jpg"
IMAGE_PATH = SAVE_DIR / SAVE_FILENAME

# --- Functions ---

def download_image(url, save_path):
    """Downloads an image from the URL and saves it to the specified path."""
    print(f"-> Attempting to download image from: {url}")
    try:
        # Ensure the save directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Make the request with a timeout and stream=True
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status() # Raise exception for bad status codes

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

def get_desktop_environment():
    """Detects the current desktop environment."""
    # Standard environment variable
    desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').upper()
    if desktop:
        print(f"-> Detected desktop environment: {desktop}")
        # Handle variations like X-Cinnamon
        if "CINNAMON" in desktop:
            return "CINNAMON"
        if "MATE" in desktop:
            return "MATE"
        if "XFCE" in desktop:
            return "XFCE"
        # Add checks for other DEs if needed (GNOME, KDE, etc.)

    # Fallback checks if XDG_CURRENT_DESKTOP is not set or specific enough
    if shutil.which("cinnamon"):
         print("-> Detected desktop environment: CINNAMON (fallback check)")
         return "CINNAMON"
    if shutil.which("mate-session"):
         print("-> Detected desktop environment: MATE (fallback check)")
         return "MATE"
    if shutil.which("xfce4-session"):
         print("-> Detected desktop environment: XFCE (fallback check)")
         return "XFCE"

    print("!! Could not reliably detect desktop environment.", file=sys.stderr)
    return None


def set_linux_background(image_path):
    """Sets the desktop background based on the detected Linux DE."""
    print(f"-> Attempting to set background to: {image_path}")
    abs_image_path = str(image_path.resolve())

    if not image_path.is_file():
        print(f"!! Error: Image file not found at {abs_image_path}", file=sys.stderr)
        return False

    de = get_desktop_environment()
    command = []

    if de == "CINNAMON":
        # Cinnamon uses gsettings with a 'file://' URI
        command = [
            "gsettings", "set",
            "org.cinnamon.desktop.background", "picture-uri",
            f"file://{abs_image_path}"
        ]
    elif de == "MATE":
        # MATE uses gsettings with just the path
         command = [
            "gsettings", "set",
            "org.mate.background", "picture-filename",
            abs_image_path
        ]
        # Older MATE might use dconf, uncomment if gsettings fails:
        # command = ["dconf", "write", "/org/mate/desktop/background/picture-filename", f"'{abs_image_path}'"]
    elif de == "XFCE":
        # XFCE uses xfconf-query. Need to set the property for the current workspace/monitor.
        # This command usually works for the primary display.
         try:
            # Get the list of properties underxfce4-desktop backdrop
            result = subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-l'], capture_output=True, text=True, check=True)
            props = result.stdout.splitlines()

            # Find properties related to the background image setting
            image_props = [p for p in props if 'last-image' in p or 'image-path' in p] # last-image is common

            if not image_props:
                 print("!! Error: Could not find XFCE background properties via xfconf-query.", file=sys.stderr)
                 return False

            # Set the background for all found properties (handles multi-monitor setups better)
            success = True
            for prop in image_props:
                print(f"   -> Setting XFCE property: {prop}")
                command = ["xfconf-query", "-c", "xfce4-desktop", "-p", prop, "-s", abs_image_path]
                run_command(command) # Use the helper function
                # We don't stop on failure for one prop, try others

            return True # Return True if we attempted to set any props

         except FileNotFoundError:
             print("!! Error: 'xfconf-query' command not found. Is XFCE installed correctly?", file=sys.stderr)
             return False
         except subprocess.CalledProcessError as e:
             print(f"!! Error running xfconf-query to list properties: {e}", file=sys.stderr)
             return False
         except Exception as e:
              print(f"!! An unexpected error occurred during XFCE setup: {e}", file=sys.stderr)
              return False

    else:
        print(f"!! Error: Unsupported or undetected desktop environment: {de}", file=sys.stderr)
        print("   Please manually set the background using your desktop's settings tool.", file=sys.stderr)
        return False

    # Execute the command for Cinnamon or MATE
    if command:
       return run_command(command)
    else:
        return False # Should not happen if DE was identified but no command generated

def run_command(command_list):
    """Helper function to run a command and check the result."""
    print(f"   -> Executing: {' '.join(command_list)}")
    try:
        result = subprocess.run(command_list, check=True, capture_output=True, text=True)
        print(f"   -> Command executed successfully.")
        # print(f"   -> STDOUT: {result.stdout}") # Uncomment for debugging
        # print(f"   -> STDERR: {result.stderr}") # Uncomment for debugging
        return True
    except FileNotFoundError:
        print(f"!! Error: Command not found: {command_list[0]}. Is it installed and in PATH?", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"!! Error executing command: {' '.join(command_list)}", file=sys.stderr)
        print(f"   Return Code: {e.returncode}", file=sys.stderr)
        print(f"   STDERR: {e.stderr}", file=sys.stderr)
        print(f"   STDOUT: {e.stdout}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"!! An unexpected error occurred running the command: {e}", file=sys.stderr)
        return False

# --- Main Execution ---

if __name__ == "__main__":
    print("--- NOAA GOES-19 Background Setter (Linux) ---")

    if download_image(NOAA_IMAGE_URL, IMAGE_PATH):
        # Brief pause might help ensure DE picks up the change immediately
        time.sleep(1)
        if not set_linux_background(IMAGE_PATH):
             print("!! Background could not be set automatically.")
    else:
        print("!! Background not updated due to download failure.")

    print("--- Script finished ---")
