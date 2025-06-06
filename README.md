ServerStats
This personal project provides a convenient way to track and visualize statistics from your Minecraft server. It automates the process of extracting JSON data from your server, backing it up to OneDrive, and then presenting that information on a locally hosted webpage using Flask.

Features
Automated Data Extraction: Regularly pulls essential JSON files directly from your Minecraft server.
OneDrive Integration: Securely copies your server's statistical data to OneDrive for easy access and backup.
Web-Based Visualization: Decodes the JSON data and displays it on a user-friendly, locally hosted webpage powered by Flask.
Customizable: Easily adaptable to monitor various Minecraft server statistics.
How it Works
The project consists of two primary Python scripts:

pull_and_copy.py (or similar): This script is responsible for:

Locating the relevant JSON files on your Minecraft server (e.g., usercache.json, stats/).
Reading the contents of these files.
Copying the JSON data to a specified location on your OneDrive.
You'll likely want to schedule this script to run periodically (e.g., using Cron on Linux or Task Scheduler on Windows) to keep your data up-to-date.
display_stats.py (or similar): This script handles the visualization:

Accessing the JSON files stored on your OneDrive.
Decoding the JSON data.
Using the Flask web framework to create a local web server.
Rendering the decoded information onto a webpage, allowing you to view your server's statistics in your web browser.
Getting Started
Prerequisites
Python 3.x
Access to your Minecraft server's file system.
OneDrive account configured on the machine running the scripts.
pip package manager.
Installation
Clone the repository:

Bash

git clone https://github.com/[YourUsername]/ServerStats.git
cd ServerStats
Install dependencies:

Bash

pip install Flask # You may need other libraries for OneDrive interaction or specific JSON parsing
Configuration
Update script paths: You'll need to modify the Python scripts (pull_and_copy.py and display_stats.py) to specify:

The exact paths to your Minecraft server's JSON files.
The target directory on your OneDrive where you want to store the data.
Consider using environment variables or a separate configuration file to manage these paths more cleanly.
OneDrive Authentication: Depending on how you're interacting with OneDrive (e.g., direct file system access if synced, or an API), you may need to configure authentication.

Running the Scripts
Run the data extraction script:

Bash

python pull_and_copy.py
For continuous monitoring, set this up as a scheduled task on your system.
Run the web server script:

Bash

python display_stats.py
Once running, open your web browser and navigate to http://127.0.0.1:5000 (or whatever address/port Flask indicates) to view your server statistics.
Contributing
This is a personal project, but suggestions and improvements are always welcome! Feel free to open an issue or submit a pull request.

License
[Choose a license and add it here, e.g., MIT, Apache 2.0, etc.]
