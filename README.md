# Reddit Chat PDF Generator

A Python script that reads a JSON file of chat messages and converts them into one or more PDF documents. The script supports embedding images referenced in the chats and includes progress logs, page numbering, and automatic PDF splitting when a specified page limit is reached.

This was specifically designed to dove-tail with the excellent [Rexit](https://github.com/MPult/Rexit) - taking all your exported Reddit chats and images, and combining them into a single entity.

## Features

- **PDF Generation:** Converts chat messages stored in a JSON file to a PDF document.
- **Image Handling:** Detects image references (URLs starting with `mxc://`) and inserts the corresponding images from the `images` directory.
- **Multiple PDFs:** Automatically creates multiple PDF files if the content exceeds a specified number of pages.
- **Page Numbers:** Adds page numbers to the bottom of each page.
- **Aspect Ratio Preservation:** Resizes images to fit within set maximum dimensions and available page space while maintaining their aspect ratio.
- **Progress Logging:** Prints status messages to the console so you know what the script is doing.

## Prerequisites

- **Python 3.x**  
- **ReportLab:** Used for PDF generation  
- **Pillow:** Used for image processing

## Installation

1. **Clone the Repository:**
   ```powershell
   git clone <repository-url>
   cd <repository-directory>
2. (optional) Create and Activate a Virtual Environment, eg:
```
python -m venv venv
venv\Scripts\activate
```

3. Install Required Packages:
```
pip install reportlab pillow
Usage
```

## Usage

1. Prepare Your Input Files:

Create a chats.json file with your chat messages. Each chat should follow a structure similar to:
```json
[
        {
          "author": "T",
          "timestamp": "2025-02-22T00:25:15Z",
          "content": {
            "Message": "And viewed by a couple thousand people..."
          }
        },
        {
          "author": "T",
          "timestamp": "2025-02-22T00:24:07Z",
          "content": {
            "Message": "Yeah I agree. 😤"
          }
        },
        {
          "author": "S",
          "timestamp": "2025-02-21T14:35:32Z",
          "content": {
            "Message": "Oh wow!!! That's so hot"
          }
        }
]
```

For image references, the message should start with mxc://. For example:
```json
{
  "author": "S",
  "timestamp": "2025-02-20T16:56:42Z",
  "content": {
    "Message": "mxc://reddit.com/7kudcgs9rbke1"
  }
}
```
Place all images in the images directory. Ensure the image file name begins with the identifier extracted from the URL.

```plaintext
project-root/
├── chat_to_pdf.py      # Your main Python script
├── chats.json          # JSON file containing chat messages
└── images/             # Directory containing all image files
    ├── 7kudcgs9rbke1.jpg
    ├── 7kudcgs9rbke2.png
    └── ...             # Additional image files
```

Run the Script:

```
python generate_pdf.py
```

The script will process your JSON file, insert images as necessary, and produce one or more PDF files (e.g., output.pdf, output_2.pdf, etc.). Progress messages will be printed to the console.

### Configuration
You can adjust various settings directly in the script:

- IMAGES_DIR: Directory where images are stored (default: images).
- MAX_PAGES_PER_PDF: Maximum number of pages per PDF file (default: 10).
- Margins and Spacing: Adjust LEFT_MARGIN, TOP_MARGIN, BOTTOM_MARGIN, TEXT_LEADING, and IMAGE_PADDING as needed.

### Git Configuration

A sample .gitignore is included to prevent the following from being committed:

- Output PDF files (output.pdf, output_*.pdf)
- The images directory
- The chats.json file
  
### License
This project is licensed under the MIT License.






