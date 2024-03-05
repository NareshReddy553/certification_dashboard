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
    
def extract_text_by_coordinates(pdf_path, x1, y1, x2, y2):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text from the specified coordinates
            text_objects = page.crop((x1, y1, x2, y2)).extract_text()
            extracted_text += text_objects.strip() + "\n"
    return extracted_text



def get_text_with_coordinates(pdf_path, search_text):
    text_coordinates = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for obj in page.extract_words():
                text = obj['text']
                if search_text in text:
                    x0, top, x1, bottom = obj['x0'], obj['top'], obj['x1'], obj['bottom']
                    text_coordinates.append({
                        'page_number': page.page_number,
                        'text': text,
                        'bounding_box': (x0, top, x1, bottom)
                    })
    return text_coordinates