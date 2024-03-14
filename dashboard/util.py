import hashlib

import pdfplumber


def calculate_sha256(file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # Read in 64KB chunks
                if not data:
                    break
                sha256_hash.update(data)
        return sha256_hash.hexdigest()
    
# def extract_text_by_coordinates(pdf_path, x1, y1, x2, y2):
#     extracted_text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             # Extract text from the specified coordinates
#             text_objects = page.crop((x1, y1, x2, y2)).extract_text()
#             extracted_text += text_objects.strip() + "\n"
#     return extracted_text

def extract_text_by_coordinates(pdf_path, coordinates_mapping):
    extracted_texts = {}
    with pdfplumber.open(pdf_path) as pdf:
        for entity, coordinates in coordinates_mapping.items():
            extracted_text = ""
            for page in pdf.pages:
                x1, y1, x2, y2 = coordinates
                # Extract text from the specified coordinates
                text_objects = page.crop((x1, y1, x2, y2)).extract_text()
                extracted_text += text_objects.strip() + "\n"
            extracted_texts[entity] = extracted_text.strip() 
    return extracted_texts



# def get_text_with_coordinates(pdf_path, search_text):
#     text_coordinates = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             for obj in page.extract_words():
#                 text = obj['text']
#                 if search_text in text:
#                     x0, top, x1, bottom = obj['x0'], obj['top'], obj['x1'], obj['bottom']
#                     text_coordinates.append({
#                         'page_number': page.page_number,
#                         'text': text,
#                         'bounding_box': (x0, top, x1, bottom)
#                     })
#     return text_coordinates


import fitz  # PyMuPDF

def get_text_with_coordinates(file_path, target_text):
    # Open the PDF file
    pdf_document = fitz.open(file_path)

    # Initialize a list to store text with coordinates
    text_with_coordinates = []

    # Iterate through each page of the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)

        # Search for the target text on the page
        text_instances = page.search_for(target_text)

        # If the target text is found on the page, extract it along with its coordinates
        for text_instance in text_instances:
            text_with_coordinates.append({
                'text': target_text,
                'page_num': page_num + 1,
                'coordinates': {
                    'x0': text_instance[0],
                    'y0': text_instance[1],
                    'x1': text_instance[2],
                    'y1': text_instance[3]
                }
            })

    # Close the PDF file
    pdf_document.close()

    return text_with_coordinates