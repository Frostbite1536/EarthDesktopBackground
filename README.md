# 🌍 Earth Desktop Background

Automatically update your desktop wallpaper with the latest **[GEOCOLOR](https://www.star.nesdis.noaa.gov/GOES/fulldisk.php?sat=G19)** satellite image from **NOAA GOES-19**. This repository includes cross-platform Python scripts for both **Windows 10/11** and **Linux Mint** (Cinnamon, MATE, XFCE).
<p align="center">
  <img width="452" alt="20250972120_GOES19-ABI-FD-GEOCOLOR-1808x1808" src="https://github.com/user-attachments/assets/0925220b-cd08-49c4-a1a3-c036af7ccfb3" />
</p>

---

## 📦 Contents

- Set_NOAA_Background_Windows.py: Script for Windows systems.
- Set_NOAA_Background_Linux.py: Script for Linux Mint and similar distributions.

---

## 🛰️ Features

- ✅ Downloads the latest NOAA GOES-19 satellite image.
- ✅ Saves it locally (in AppData on Windows or ~/.cache on Linux).
- ✅ Automatically sets the image as your desktop wallpaper.
- ✅ Supports multiple Linux desktop environments.
- ✅ Includes error handling and verbose output.

---

## 🪟 Windows Instructions

### 1. Install Python

Download and install [Python from python.org](https://www.python.org/). Ensure you select **"Add Python to PATH"** during installation.

### 2. Install Required Library

Open **Command Prompt** or **PowerShell** and run:

```bash
pip install requests
```

### 3. Run the Script

```bash
python Set_NOAA_Background_Windows.py
```

You should see output messages indicating download and wallpaper update status.

### 4. Optional: Schedule with Task Scheduler

To automate the wallpaper update:
* Open **Task Scheduler**
* Create a new basic task:
   * **Trigger**: Daily or every X minutes
   * **Action**: Start a program
      * Program: `pythonw.exe`
      * Arguments: `C:\path\to\Set_NOAA_Background_Windows.py`
      * Start in: `C:\path\to\`

## 🐧 Linux Instructions

### 1. Install Required Library

```bash
pip3 install requests
```

Alternatively:

```bash
sudo apt update && sudo apt install python3-requests
```

### 2. Save and Make Script Executable

```bash
chmod +x Set_NOAA_Background_Linux.py
```

### 3. Run the Script

```bash
./Set_NOAA_Background_Linux.py
```

Or:

```bash
python3 Set_NOAA_Background_Linux.py
```

The script detects your desktop environment (Cinnamon, MATE, XFCE) and applies the wallpaper using appropriate tools (`gsettings`, `xfconf-query`).

### 4. Optional: Automate with Cron

To update every 15 minutes:

```bash
crontab -e
```

Add:

```cron
*/15 * * * * /usr/bin/python3 /absolute/path/to/Set_NOAA_Background_Linux.py > /dev/null 2>&1
```

Replace `/absolute/path/to/` with the actual path to your script.

## 🛠️ Next Steps & Improvements

* Add GUI.
* Allow selection of resolution or image type.
* Improve multi-monitor support for XFCE and other DEs.
* Add persistent logging to file instead of console output.

## 🖼️ Image Source

All images come from NOAA's public GOES-19 satellite feed:
https://cdn.star.nesdis.noaa.gov/GOES19/ABI/FD/GEOCOLOR/latest.jpg

## 🤝 Contributions

Pull requests and suggestions are welcome! If you want to extend support to additional Linux desktop environments (like GNOME or KDE), feel free to contribute.
