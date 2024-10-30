### Automatic File Organizer

This is a Python application built with Tkinter to help organize files from a source directory to a destination directory. It categorizes files based on type, creation date, and file size, with options for moving or copying files and automatic compression of large files.

## Features

	•	Automatic Organization: Sorts files into folders by file type (Images, Videos, Documents, Others) and by month of creation.
	•	Move or Copy: Choose between moving files (removing from source) or copying files (keeping source intact).
	•	Duplicate Detection: Uses MD5 hashing to skip duplicate files in the destination.
	•	Compression for Large Files: Automatically compresses files larger than 10 MB.
	•	Progress Tracking: Displays progress and status updates as files are organized.

### Getting Started

## Prerequisites

Make sure you have Python 3 installed. The following standard libraries are used:

	•	os
	•	shutil
	•	datetime
	•	hashlib
	•	zipfile
	•	mimetypes
	•	threading
	•	tkinter

No external dependencies are required.

## Installation

	1.	Clone the repository:

git clone https://github.com/yourusername/automatic-file-organizer.git


	2.	Navigate to the project directory:

cd automatic-file-organizer


	3.	Run the application:

python file_organizer.py



## Usage

	1.	Launch the application.
	2.	Use the Browse buttons to select a source folder (containing files to organize) and a destination folder (where organized files will be stored).
	3.	Check or uncheck the “Move files instead of copying” option to choose your preferred file handling method.
	4.	Click Organize Files to start the organization process.

The application will categorize files by type and creation date, remove duplicates, and compress any files over 10 MB.

## Code Overview

## FileOrganizerGUI Class

	•	create_widgets(): Sets up the graphical user interface elements, including labels, buttons, and the progress bar.
	•	browse_source() and browse_dest(): Opens a file dialog for source and destination folder selection.
	•	start_organizing_files(): Begins the file organization in a new thread.
	•	organize_files(): Main method for organizing files, managing the progress bar and error handling.
	•	process_file(): Moves or copies files, skips duplicates, and compresses large files.
	•	Helper Methods:
	•	get_file_type(): Determines file type based on MIME type.
	•	get_file_date(): Retrieves the file’s creation date for subfolder categorization.
	•	get_file_hash(): Calculates the MD5 hash of a file for duplicate detection.
	•	compress_file(): Compresses files over 10 MB into a .zip file and removes the original.

## File Organization Structure

Files in the destination directory will be organized as follows:

Destination_Folder/
├── Documents/
│   ├── 2023-01/
│   │   └── example.pdf
│   └── 2023-02/
│       └── example.docx
├── Images/
│   └── 2023-01/
│       └── example.jpg
├── Videos/
│   └── 2023-03/
│       └── example.mp4
└── Others/
    └── 2023-01/
        └── example.txt

# Notes

	•	Duplicate files with matching MD5 hashes in the destination will be skipped.
	•	Files larger than 10 MB will be compressed into .zip archives to save space.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch for your changes, and submit a pull request.

## Contact

For any questions or feedback, please reach out via GitHub Issues.
