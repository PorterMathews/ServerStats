# ServerStats

This personal project provides a dynamic way to track and visualize statistics from your Minecraft server. It orchestrates the automated extraction of JSON data from your server, backs it up to your OneDrive, and then presents that information on a user-friendly, locally hosted webpage using Flask.

---

## Features

* **Automated Server Data Backup:** `ServerPush.py` automatically pulls essential JSON files from your Minecraft server and copies them to your OneDrive every 5 minutes.
* **OneDrive Integration:** Securely stores your server's statistical data on OneDrive for easy access and robust backup.
* **Web-Based Visualization:** `Processing.py` reads the JSON data from OneDrive, decodes it, resolves player UUIDs to current usernames using Mojang's API, and displays it on a local webpage via Flask.
* **On-Demand Data Display:** The web visualization script runs manually, allowing you to view updated statistics whenever you need them.
* **Customizable:** Easily adaptable to monitor various Minecraft server statistics by adjusting file paths in `settings.py`.

---

## How it Works

The project consists of two primary Python scripts designed to work in conjunction:

1.  **`ServerPush.py`:**
    This script is responsible for the continuous synchronization of your Minecraft server data to OneDrive.
    * It locates the specified JSON files on your Minecraft server (e.g., player statistics, user cache).
    * Copies these files to a designated directory on your OneDrive.
    * This process is automated to run every 5 minutes in the background, ensuring your OneDrive data is kept up-to-date.

2.  **`Processing.py`:**
    This script handles the retrieval and presentation of the statistics from your OneDrive.
    * It reads all JSON files from the specified OneDrive directory.
    * Decodes the JSON content and, importantly, resolves Minecraft player UUIDs (Universally Unique Identifiers) to their current usernames by querying the Mojang API.
    * Utilizes the Flask web framework to create a local web server.
    * Renders the processed information onto an HTML template (`PlayerStats.html`), allowing you to view your server's statistics directly in your web browser. This script is intended to be run manually when you wish to view the stats.

---

## Getting Started

### Prerequisites

* Python 3.x
* Access to your Minecraft server's file system (for `ServerPush.py`).
* OneDrive account configured and synced on the machine running the scripts, allowing local file access.
* `pip` package manager.
* Internet connection for `Processing.py` to resolve UUIDs via Mojang API.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YourUsername]/ServerStats.git
    cd ServerStats
    ```

2.  **Install dependencies:**
    ```bash
    pip install Flask requests
    ```

### Configuration

You **must** create a `settings.py` file in the root directory of this project (same directory as `ServerPush.py` and `Processing.py`). This file will contain the necessary paths for both scripts to function correctly.

`settings.py` example:

```python
# settings.py

# --- For ServerPush.py ---
# Path to the Minecraft server files you want to copy (e.g., a specific stats file or a directory)
FILEPATH_TO_SERVER = "C:\\Path\\To\\Your\\MinecraftServer\\world\\stats" # Example: directory for all player stats JSONs

# Path to your OneDrive directory where you want to store the copied files
FILEPATH_TO_STORAGE = "C:\\Users\\YourUsername\\OneDrive\\MinecraftServerStatsBackup"

# --- For Processing.py ---
# Path to the directory on your OneDrive where the Minecraft stats JSONs are stored by ServerPush.py
STATS_PATH = "C:\\Users\\YourUsername\\OneDrive\\MinecraftServerStatsBackup"
