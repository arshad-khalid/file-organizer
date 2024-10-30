import os
import shutil
import datetime
import hashlib
import zipfile
import mimetypes
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

class FileOrganizerGUI:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        master.title("Automatic File Organizer")
        master.geometry("750x320")

        # Option to choose between moving and copying files
        self.move_files = tk.BooleanVar()
        self.move_files.set(True)

        # Create and display the GUI widgets
        self.create_widgets()

    def create_widgets(self):
        # Source folder selection
        self.source_label = tk.Label(self.master, text="Source Folder:")
        self.source_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.source_entry = tk.Entry(self.master, width=50)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10)

        self.source_button = tk.Button(self.master, text="Browse", command=self.browse_source)
        self.source_button.grid(row=0, column=2, padx=10, pady=10)

        # Destination folder selection
        self.dest_label = tk.Label(self.master, text="Destination Folder:")
        self.dest_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.dest_entry = tk.Entry(self.master, width=50)
        self.dest_entry.grid(row=1, column=1, padx=10, pady=10)

        self.dest_button = tk.Button(self.master, text="Browse", command=self.browse_dest)
        self.dest_button.grid(row=1, column=2, padx=10, pady=10)

        # Move or Copy Option
        self.move_option = tk.Checkbutton(self.master, text="Move files instead of copying", variable=self.move_files)
        self.move_option.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Organize button to initiate file organization
        self.organize_button = tk.Button(self.master, text="Organize Files", command=self.start_organizing_files)
        self.organize_button.grid(row=3, column=1, pady=20)

        # Progress bar to show file organization progress
        self.progress = ttk.Progressbar(self.master, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Status label to display current status or messages
        self.status_label = tk.Label(self.master, text="")
        self.status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def browse_source(self):
        # Function to select source folder
        folder_path = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, folder_path)

    def browse_dest(self):
        # Function to select destination folder
        folder_path = filedialog.askdirectory()
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, folder_path)

    def start_organizing_files(self):
        # Start organizing files in a new thread
        threading.Thread(target=self.organize_files).start()

    def organize_files(self):
        # Main function to organize files from source to destination folder
        source_folder = self.source_entry.get()
        destination_folder = self.dest_entry.get()

        if not source_folder or not destination_folder:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return

        try:
            # Reset progress bar and update status
            self.progress['value'] = 0
            self.status_label.config(text="Organizing files...")
            self.master.update()

            # Calculate total number of files for progress tracking
            file_count = sum([len(files) for r, d, files in os.walk(source_folder)])
            processed_files = 0

            # Process each file in the source directory
            for root, _, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.process_file(file_path, destination_folder)
                    processed_files += 1
                    # Update progress bar and status label
                    self.progress['value'] = (processed_files / file_count) * 100
                    self.status_label.config(text=f"Processing file: {file}")
                    self.master.update()

            # Show completion message
            self.status_label.config(text="File organization completed!")
            messagebox.showinfo("Success", "File organization completed!")
        except Exception as e:
            # Show error message if an exception occurs
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def process_file(self, file_path, destination_folder):
        # Processes a single file by moving it to organized subfolders
        file_type = self.get_file_type(file_path)    # Determine file type (e.g., Images, Documents)
        file_date = self.get_file_date(file_path)    # Determine file creation date (formatted as YYYY-MM)
        file_hash = self.get_file_hash(file_path)    # Calculate file hash for duplicate detection

        # Create subfolders based on file type and date
        subfolder = os.path.join(destination_folder, file_type, file_date)
        os.makedirs(subfolder, exist_ok=True)

        new_file_path = os.path.join(subfolder, os.path.basename(file_path))

        # Skip file if it's a duplicate
        if os.path.exists(new_file_path) and self.get_file_hash(new_file_path) == file_hash:
            self.status_label.config(text=f"Skipping duplicate: {file_path}")
            return

        # Copy or move file based on user selection
        if self.move_files.get():
            shutil.move(file_path, new_file_path)
        else:
            shutil.copy2(file_path, new_file_path)

        # Compress file if size is larger than 10 MB
        if os.path.getsize(new_file_path) > 10 * 1024 * 1024:
            self.compress_file(new_file_path)

    def get_file_type(self, file_path):
        # Determine the file type based on extension or mimetype
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith("image"):
                return 'Images'
            elif mime_type.startswith("application"):
                return 'Documents'
            elif mime_type.startswith("video"):
                return 'Videos'
        return 'Others'

    def get_file_date(self, file_path):
        # Get file creation date and format as YYYY-MM
        timestamp = os.path.getctime(file_path)
        date = datetime.datetime.fromtimestamp(timestamp)
        return date.strftime('%Y-%m')

    def get_file_hash(self, file_path):
        # Calculate MD5 hash of a file to detect duplicates
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def compress_file(self, file_path):
        # Compress the file if it exceeds size limit (10 MB)
        try:
            zip_path = file_path + '.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, os.path.basename(file_path))
            os.remove(file_path)  # Remove original file after compressing
            self.status_label.config(text=f"Compressed large file: {file_path}")
        except Exception as e:
            self.status_label.config(text=f"Failed to compress {file_path}: {str(e)}")

# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()