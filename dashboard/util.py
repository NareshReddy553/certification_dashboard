from difflib import get_close_matches
import hashlib
import pdfplumber
import fitz
import re
import logging

logger = logging.getLogger(__name__)



def calculate_sha256(file_path):
    logger.info("Calculating SHA-256 hash for file: %s", file_path)
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


def get_text_with_coordinates(file_path, target_text):
    text_with_coordinates = []
    with fitz.open(file_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text_instances = page.search_for(target_text)
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
    return text_with_coordinates


def extract_and_split_text_from_pdf(pdf_path):
    desired_data = {}
    with fitz.open(pdf_path) as doc:
        page = doc[0]
        text = page.get_text()
        words = text.split()
        if words:
            # Extract student ID
            student_id = words[words.index('ID:') + 1]
            desired_data['student_id'] = re.sub(r'\([^)]*\)', '', student_id)
            # Extract student name
            start_index = words.index('that')
            end_index = words.index('(Student')
            student_name = words[start_index + 1:end_index]
            desired_data['student_name'] = ' '.join(student_name).strip()
            # Extract student grade
            grade_index = words.index('Grade')
            desired_data['grade'] = words[grade_index + 1]
            # Extract student semester
            sem_index = words.index('Semester')
            desired_data['semester'] = re.sub(r'\D', '', words[sem_index - 1])
            # Extract certificate issued date
            issued_index = words.index('Issued')
            issued_date = words[issued_index - 3:issued_index]
            desired_data['issued_date'] = ' '.join(issued_date).strip()
            # Extract certificate completion date
            completion_index = words.index('Issued')
            completion_date = words[completion_index + 2:completion_index + 5]
            desired_data['completion_date'] = ' '.join(completion_date).strip()
            # Extract student course
            course_start_index = words.index('titled')
            matches = get_close_matches("offered", words, n=1)
            course_end_index = words.index(matches[0] if matches else 'ofered')
            course_name = words[course_start_index + 1:course_end_index]
            desired_data['course'] = ' '.join(course_name).strip()
            # Extract student department
            department_start_index = words.index('in')
            department_end_index = words.index('Grade')
            department_name = words[department_start_index + 1:department_end_index]
            desired_data['department'] = ' '.join(department_name).strip()
        return desired_data



def extract_course_name(text):
    parts = text.split("offered by", 1)
    course_name = parts[0].strip()
    return course_name

def extract_department_degree_names(text):
    parts = re.split(r'\b(in)\b', text, 1)
    if len(parts) > 1:
        degree_name = parts[0].strip()
        department_name = parts[2].strip()
        return degree_name, department_name
    else:
        return None, None

def extract_student_id(text):
    pattern = r"Student ID: ([A-Za-z0-9]+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

    
def extract_certificate_id(text):
    pattern = r"Certifcate ID ([A-Za-z0-9]+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None