import tkinter as tk
from tkinter import filedialog
import os
import shutil
from collections import defaultdict

# Dictionary of extensions and corresponding folders
extensions = {
    "jpg": "images",
    "png": "images",
    "ico": "images",
    "gif": "images",
    "svg": "images",
    "webp":"images",
    "docx": "word",
    "sql": "sql",
    "exe": "programs",
    "msi": "programs",
    "pdf": "pdf",
    "xlsx": "excel",
    "csv": "excel",
    "rar": "archive",
    "zip": "archive",
    "gz": "archive",
    "tar": "archive",
    "torrent": "torrent",
    "txt": "text",
    "ipynb": "python",
    "py": "python",
    "pptx": "powerpoint",
    "ppt": "powerpoint",
    "mp3": "audio",
    "wav": "audio",
    "mp4": "video",
    "m3u8": "video",
    "webm": "video",
    "ts": "video",
    "json": "json",
    "css": "web",
    "js": "web",
    "html": "web",
    "apk": "apk",
    "sqlite3": "sqlite3",
}

# Function to organize files into folders based on extensions
def organize_files(directory_path):
    counts = defaultdict(int)
    moved_files = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            file_extension = filename.split('.')[-1].lower()

            # Get the destination folder based on the extension
            destination_folder = extensions.get(file_extension, 'Other')

            # Create the destination folder if it doesn't exist
            destination_path = os.path.join(directory_path, destination_folder)
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

            # Move the file to the appropriate folder
            shutil.move(file_path, os.path.join(destination_path, filename))
            counts[destination_folder] += 1
            moved_files.append(filename)

    return counts, moved_files

# Function to handle the directory selection
def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        original_counts, moved_files = organize_files(directory_path)
        status_label.config(text=f"Files in '{directory_path}' organized successfully!")

        # Display the counts and moved files
        counts_label.config(text="Files moved to each folder:")
        for folder, count in original_counts.items():
            moved_label = tk.Label(main_frame, text=f"{folder}: {count} files")
            moved_label.pack()
        
        undo_button.config(state=tk.NORMAL)
        undo_button.config(command=lambda: undo(directory_path, moved_files))

# Function to undo the file organization
def undo(directory_path, moved_files):
    for filename in moved_files:
        source_path = os.path.join(directory_path, filename)
        original_extension = filename.split('.')[-1].lower()
        original_folder = extensions.get(original_extension, 'Other')
        destination_path = os.path.join(directory_path, original_folder, filename)
        shutil.move(destination_path, source_path)

    undo_button.config(state=tk.DISABLED)
    status_label.config(text="Undo complete. Files restored to their original locations.")
    counts_label.config(text="")

# Create the main application window
root = tk.Tk()
root.title("File Organizer")

# Create and configure the main frame
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack()

# Create and configure a label
label = tk.Label(main_frame, text="Select a directory to organize:")
label.pack()

# Create and configure a button to select a directory
select_button = tk.Button(main_frame, text="Select Directory", command=select_directory)
select_button.pack()

# Create and configure a label for status messages
status_label = tk.Label(main_frame, text="")
status_label.pack()

# Create and configure a label for file counts
counts_label = tk.Label(main_frame, text="")
counts_label.pack()

# Create and configure an "Undo" button
undo_button = tk.Button(main_frame, text="Undo", state=tk.DISABLED)
undo_button.pack()

root.mainloop()
