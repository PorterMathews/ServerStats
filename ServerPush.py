import shutil
import os
import threading
import time
import sys

# Import the hardcoded file paths from a settings.py file
# Ensure that settings.py exists in the same directory and contains:
# FILEPATH_TO_STORAGE = "/path/to/your/storage/directory"
# FILEPATH_TO_SERVER = "/path/to/your/server/file.txt"
from settings import FILEPATH_TO_STORAGE, FILEPATH_TO_SERVER

# Define the interval for repeating the file move (5 minutes = 300 seconds)
INTERVAL_SECONDS = 300

def move_file():
    """
    Moves a file from the hardcoded source_path (FILEPATH_TO_SERVER)
    to the hardcoded destination_path (FILEPATH_TO_STORAGE).
    If a file already exists at the destination_path, it will be overwritten.
    """
    source_path = FILEPATH_TO_SERVER
    destination_path = FILEPATH_TO_STORAGE

    print(f"Attempting to move '{source_path}' to '{destination_path}' at {time.ctime()}...")

    try:
        # Check if the source file exists
        if not os.path.exists(source_path):
            print(f"Error: Source file not found at '{source_path}'")
            return False # Indicate failure

        # If the destination path is an existing directory,
        # we want to move the file into that directory, keeping its original name.
        # Otherwise, the destination_path is treated as the new full path including filename.
        if os.path.isdir(destination_path):
            destination_filename = os.path.basename(source_path)
            destination_path = os.path.join(destination_path, destination_filename)

        # Use shutil.move to move the file.
        # It automatically handles overwriting if the destination is a file.
        shutil.move(source_path, destination_path)
        print(f"Successfully moved '{source_path}' to '{destination_path}'")
        return True # Indicate success

    except FileNotFoundError:
        print(f"Error: One of the paths specified was not found.")
        return False
    except PermissionError:
        print(f"Error: Permission denied. Check file/folder permissions for '{source_path}' and '{destination_path}'.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def schedule_move():
    """
    Schedules the move_file function to run after INTERVAL_SECONDS,
    and then reschedules itself.
    """
    # Call the file moving function
    move_file()
    # Schedule the next call
    global timer_thread
    timer_thread = threading.Timer(INTERVAL_SECONDS, schedule_move)
    timer_thread.start()

# --- Main execution block ---
if __name__ == "__main__":
    print(f"Starting file mover. It will run every {INTERVAL_SECONDS / 60} minutes.")
    print("Press Ctrl+C to stop the script.")

    # Initialize the timer_thread globally to be able to cancel it
    timer_thread = None

    try:
        # Start the first scheduled move immediately
        schedule_move()
        # Keep the main thread alive so the timer thread can run
        # This loop will run indefinitely until a KeyboardInterrupt
        while True:
            time.sleep(1) # Sleep for a short duration to avoid busy-waiting
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Stopping the file mover...")
        if timer_thread:
            timer_thread.cancel() # Cancel the pending timer
        print("Script stopped.")
        sys.exit(0) # Exit gracefully
    except Exception as e:
        print(f"An unhandled error occurred in the main loop: {e}")
        if timer_thread:
            timer_thread.cancel()
        sys.exit(1)