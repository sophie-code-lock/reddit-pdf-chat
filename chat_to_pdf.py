import json
import os
import glob
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image  # used for computing image dimensions

# Register the open source Symbola font that supports words and emojis.
pdfmetrics.registerFont(TTFont('UniversalFont', 'fonts/Symbola.ttf'))

# Configuration constants
IMAGES_DIR = "images"
MAX_PAGES_PER_PDF = 10
LEFT_MARGIN = 50
BOTTOM_MARGIN = 50
TOP_MARGIN = 50  # margin from the top of the page
TEXT_LEADING = 12  # space between lines
IMAGE_PADDING = 15  # space after an image before next content

def find_image_path(image_ref, images_dir=IMAGES_DIR):
    image_id = image_ref.split("/")[-1]
    files = glob.glob(os.path.join(images_dir, image_id + ".*"))
    if files:
        return files[0]
    return None

def draw_page_number(canvas_obj, current_page, page_width):
    canvas_obj.setFont("UniversalFont", 8)
    canvas_obj.drawRightString(page_width - 50, BOTTOM_MARGIN / 2, f"Page {current_page}")

def new_canvas(pdf_index, page_size):
    filename = "output.pdf" if pdf_index == 1 else f"output_{pdf_index}.pdf"
    print(f"Creating new PDF file: {filename}")
    return canvas.Canvas(filename, pagesize=page_size), filename

def add_new_page(c, current_page, width, height, pdf_index):
    draw_page_number(c, current_page, width)
    if current_page >= MAX_PAGES_PER_PDF:
        print(f"PDF file reached {MAX_PAGES_PER_PDF} pages. Saving current PDF and starting a new one.")
        c.save()
        pdf_index += 1
        c, fname = new_canvas(pdf_index, (width, height))
        current_page = 1
    else:
        c.showPage()
        current_page += 1
    print(f"Added new page: now on page {current_page} of PDF file index {pdf_index}")
    y = height - TOP_MARGIN
    return c, current_page, pdf_index, y

def add_text(c, text, x, y, width):
    wrapped_lines = textwrap.wrap(text, width=80)
    for line in wrapped_lines:
        c.drawString(x, y, line)
        y -= TEXT_LEADING
    return y

def main():
    print("Starting PDF generation...")
    input_file = "chats.json"
    pdf_index = 1

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            chats = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file '{input_file}': {e}")
        return

    total_chats = len(chats)
    print(f"Loaded {total_chats} chat messages.")

    width, height = letter
    c, current_pdf_fname = new_canvas(pdf_index, letter)
    current_page = 1
    y = height - TOP_MARGIN

    # Process each chat message
    for i, chat in enumerate(chats):
        print(f"Processing chat {i+1}/{total_chats}...")
        if y < BOTTOM_MARGIN + 40:
            c, current_page, pdf_index, y = add_new_page(c, current_page, width, height, pdf_index)

        author = chat.get("author", "Unknown")
        timestamp = chat.get("timestamp", "")
        message = chat.get("content", {}).get("Message", "")

        header = f"{timestamp} - {author}:"
        c.setFont("UniversalFont", 10)
        c.drawString(LEFT_MARGIN, y, header)
        y -= 15

        c.setFont("UniversalFont", 10)
        if message.startswith("mxc://"):
            print(f"Chat {i+1}: Found image reference: {message}")
            image_path = find_image_path(message)
            if image_path and os.path.exists(image_path):
                try:
                    with Image.open(image_path) as im:
                        im_width, im_height = im.size
                    max_img_width = 300
                    max_img_height = 300
                    available_space = y - BOTTOM_MARGIN
                    scale = min(max_img_width / im_width,
                                max_img_height / im_height,
                                available_space / im_height)
                    new_width = im_width * scale
                    new_height = im_height * scale

                    if new_height > available_space:
                        print(f"Not enough space for image on current page. Adding a new page.")
                        c, current_page, pdf_index, y = add_new_page(c, current_page, width, height, pdf_index)

                    c.drawImage(image_path, LEFT_MARGIN, y - new_height, width=new_width, height=new_height)
                    print(f"Chat {i+1}: Image added with dimensions: {new_width:.2f}x{new_height:.2f}")
                    y -= new_height + IMAGE_PADDING
                except Exception as e:
                    print(f"Error processing image for chat {i+1}: {e}")
                    c.drawString(LEFT_MARGIN, y, f"[Error loading image: {e}]")
                    y -= 15
            else:
                print(f"Chat {i+1}: Image not found for reference: {message}")
                c.drawString(LEFT_MARGIN, y, f"[Image not found for reference: {message}]")
                y -= 15
        else:
            y = add_text(c, message, LEFT_MARGIN, y, width - 2 * LEFT_MARGIN)
            y -= 10

    draw_page_number(c, current_page, width)
    c.save()
    print("PDF generation complete.")

if __name__ == "__main__":
    main()
