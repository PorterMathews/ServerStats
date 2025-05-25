import shutil
import os
# Import the hardcoded file paths from a settings.py file
from settings import FILEPATH_TO_STORAGE, FILEPATH_TO_SERVER

def move_file():
    """
    Moves a file from the hardcoded source_path (FILEPATH_TO_SERVER)
    to the hardcoded destination_path (FILEPATH_TO_STORAGE).
    If a file already exists at the destination_path, it will be overwritten.
    """
    source_path = FILEPATH_TO_SERVER
    destination_path = FILEPATH_TO_STORAGE

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
        print(f"Error: Permission denied. Check file/folder permissions.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# --- Example Usage ---
if __name__ == "__main__":
    print("Attempting to move file using hardcoded paths from settings.py...")
    # Call the move_file function without arguments
    move_file()
    print("\n--- Script execution finished ---")