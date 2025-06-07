import json
import os
from flask import Flask, render_template
import requests

try:
    from settings import STATS_PATH
    STATS = STATS_PATH
except ImportError:
    print("Error: settings.py not found or STATS not defined.")
    print("Please create a settings.py file in the same directory as app.py and define STATS.")
    print("Example: STATS = 'C:\\path\\to\\your\\minecraft\\stats'")
    # If settings.py is missing or STATS is not defined, the app will not run correctly.
    # We'll exit here as a fallback is not appropriate for an absolute path requirement.
    exit("Configuration error: STATS not properly set in settings.py.")


def get_username_from_uuid(uuid):
    """
    Fetches the current Minecraft username for a given UUID using Mojang's API.

    Args:
        uuid (str): The player's UUID (can include hyphens).

    Returns:
        str: The player's current username, or 'Unknown Player' if not found or an error occurs.
    """
    # Mojang API expects UUIDs without hyphens if you're building certain URLs,
    # but the session server endpoint often handles them with hyphens too.
    # For consistency and robustness, let's remove hyphens.
    clean_uuid = uuid.replace('-', '')

    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{clean_uuid}"

    try:
        response = requests.get(url, timeout=5)  # Add a timeout for safety
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data.get('name', 'Unknown Player')
    except requests.exceptions.Timeout:
        print(f"Timeout while fetching username for UUID: {uuid}")
        return 'API Timeout'
    except requests.exceptions.RequestException as e:
        print(f"Error fetching username for UUID {uuid}: {e}")
        return 'API Error'
    except json.JSONDecodeError:
        print(f"Error decoding JSON for UUID: {uuid}. Response: {response.text}")
        return 'Invalid API Response'


def read_minecraft_stats():
    """
    Reads all JSON files in the specified directory and returns their content,
    including resolving UUIDs to usernames.

    Returns:
        dict: A dictionary where keys are filenames (without .json extension)
              and values are the parsed JSON content, with 'username' added.
    """
    if not os.path.exists(STATS):
        print(
            f"Error: STATS '{STATS}' does not exist. Please check your settings.py and ensure the path is correct.")
        return {}
    if not os.path.isdir(STATS):
        print(f"Error: STATS '{STATS}' is not a directory. Please provide a path to a folder.")
        return {}

    player_stats = {}
    for filename in os.listdir(STATS):
        if filename.endswith(".json"):
            filepath = os.path.join(STATS, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    player_uuid = os.path.splitext(filename)[0]  # e.g., "0a1b2c3d-e4f5-6789-abcd-ef0123456789"

                    # Resolve UUID to username
                    username = get_username_from_uuid(player_uuid)
                    data['username'] = username  # Add the username to the player's data dictionary

                    player_stats[player_uuid] = data
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {filename} at {filepath}")
            except Exception as e:
                print(f"An error occurred while reading file {filename} at {filepath}: {e}")
    return player_stats


app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the main page displaying Minecraft player stats.
    """
    stats = read_minecraft_stats()
    return render_template('PlayerStats.html', player_stats=stats)


if __name__ == '__main__':
    app.run(debug=True)