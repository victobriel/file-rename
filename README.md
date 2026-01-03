# File Rename

A powerful desktop application for batch renaming files and folders with an intuitive graphical interface. Built with Python and PySide6, File Rename provides advanced pattern-based renaming capabilities while keeping your data safe with built-in backup and path protection features.

![Python Version](https://img.shields.io/badge/Python-3.6%2B-green&style=flat")
![License](https://img.shields.io/github/license/victobriel/File-Rename)
![Downloads](https://img.shields.io/github/downloads/victobriel/File-Rename/total)

[Screenshots](#screenshots) | [Features](#features) | [Installation](#installation) | [Usage](#usage)

## Features

### Core Capabilities
* **Batch Rename** - Rename multiple files and folders simultaneously
* **Multiple Rename Modes**:
  - **Add Prefix/Suffix** - Add text before or after file names
  - **Find and Replace** - Replace specific text patterns in file names
  - **Change Extensions** - Bulk change file extensions
  - **Sequential Numbering** - Add sequential numbers to file names
* **Regex Support** - Use regular expressions for advanced pattern matching
* **Case-Sensitive/Insensitive** - Toggle case sensitivity for find operations
* **File Type Filtering**:
  - All files mode
  - Common file types (30+ categories including documents, images, videos, audio, etc.)
  - Custom file type specification
* **Folder Support** - Rename folders along with files
* **Subdirectory Processing** - Optionally include files in subdirectories
* **Real-time Preview** - See rename results before applying changes
* **Multi-language Support** - Available in English and Portuguese (Brazil)

### Safety Features
* **Automatic Backup** - Create ZIP backups before renaming
* **Protected Paths** - Built-in protection for system directories (Windows, Program Files, etc.)
* **Hidden File Protection** - Automatically skips hidden files and folders
* **Visual Confirmation** - Color-coded preview of files to be renamed

### Advanced Features
* **Date/Time Variables** - Insert current date/time in file names:
  - `{%D}` - Day
  - `{%M}` - Month
  - `{%Y}` - Year
  - `{%H}` - Hour
  - `{%I}` - Minute
* **Progress Tracking** - Real-time progress bar for large operations
* **File Statistics** - View file counts, sizes, and extensions

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Required Dependencies
```bash
pip install PySide6 pandas
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/victobriel/File-Rename.git
   cd File-Rename
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Basic Workflow

1. **Open a Folder**
   - Click the folder icon or use `File > Open Folder`
   - Select the directory containing files to rename

2. **Configure Options**
   - Choose whether to include subdirectories
   - Select to include folders in renaming
   - Enable backup before renaming (recommended)

3. **Select File Types**
   - **All Files** - Process all files
   - **Common Files** - Choose from predefined categories
   - **Specific Files** - Specify custom file extensions

4. **Choose Rename Rule**
   - **Add** - Prefix or suffix text to file names
   - **Replace** - Find and replace text patterns
   - **Change Extension** - Bulk change file extensions
   - **Add Number** - Add sequential numbering

5. **Preview Changes**
   - Review the "New Name" column
   - Files to be renamed are highlighted in blue

6. **Apply Rename**
   - Click the "Rename" button
   - Confirm the operation

### Rename Examples

**Add Prefix:**
```
Original: photo.jpg
Rule: Add "vacation_" (prefix)
Result: vacation_photo.jpg
```

**Sequential Numbering:**
```
Original: document.pdf, report.pdf, memo.pdf
Rule: Add Number starting from 1, increment by 1
Result: (1)document.pdf, (2)report.pdf, (3)memo.pdf
```

**Replace with Date:**
```
Original: report.docx
Rule: Replace "report" with "Report_{%Y}_{%M}_{%D}"
Result: Report_2026_01_03.docx
```

**Change Extension:**
```
Original: file.txt
Rule: Change extension to "md"
Result: file.md
```

**Regex Replace:**
```
Original: IMG_20240101_001.jpg
Rule: Replace "IMG_(\d{8})_(\d{3})" with "Photo_$1"
Result: Photo_20240101.jpg
```

## Configuration

The application uses `config.ini` for settings:

```ini
[config]
backup = False              # Enable automatic backups
language = en_US            # Language (en_US or pt_BR)
encoding = utf-8            # File encoding

[paths]
protect_paths = True        # Enable path protection
protected = C:/Windows,C:/Program Files,C:/ProgramData,AppData,System Volume Information
```

### Supported File Types

Over 30 categories including:
- Documents (Word, PDF, Text, etc.)
- Images (JPG, PNG, GIF, etc.)
- Videos (MP4, AVI, MKV, etc.)
- Audio (MP3, WAV, FLAC, etc.)
- Archives (ZIP, RAR, 7Z, etc.)
- Programming files (Python, JavaScript, Java, etc.)
- And many more...

## Safety & Best Practices

?? **Important Safety Tips:**
- Always test with a small batch first
- Keep the "Protect Paths" option enabled
- Use the backup feature for important files
- Review the preview carefully before renaming
- Avoid renaming system folders

## Keyboard Shortcuts

- `Enter` - Add file extension when typing in specific files field

## Troubleshooting

**Error 0x0001:** Unable to access directory
- Check folder permissions
- Disable antivirus temporarily

**Error 0x0002:** Unable to load files
- Check if files are in use by another program
- Verify read permissions

**Error 0x0003:** Unable to rename file
- File may be open in another program
- Check write permissions
- File name may contain invalid characters

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

**victobriel**
- GitHub: [@victobriel](https://github.com/victobriel)

## Acknowledgments

- Built with PySide6 (Qt for Python)
- Icons from standard icon sets
- Database of common file types

## Version History

**v1.0.0**
- Initial release
- Batch file and folder renaming
- Multiple rename modes
- Regex support
- Multi-language support
- Backup functionality
- Protected paths

## Screenshots
<img src="screenshots/main.png" alt="File-Rename Image Preview" width="500" style='text-align="center"'>

---

**Note:** Always backup important files before performing batch rename operations.
