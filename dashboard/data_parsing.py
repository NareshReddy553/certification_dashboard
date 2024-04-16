import re
from django.db import OperationalError
import fitz
import logging
from datetime import datetime, time
from dashboard.models import Certificates, Certificatetype, Course, Degree, Department, Student, StudentMarks
from dashboard.util import calculate_sha256, extract_certificate_id, extract_course_name, extract_department_degree_names, extract_student_id

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text(file_path):
    try:
        pdf_document =fitz.open(stream=file_path.read(), filetype="pdf")
        page = pdf_document.load_page(0)  # Load only the first page
        page_text = page.get_text()
        return page_text.split('\n')
    except Exception as e:
        logger.error("Error occurred while extracting text from PDF: %s", e)
        return []

def certificate_data_extraction_from_pdf(file_path):
    
    try:
        sha256_hash = calculate_sha256(file_path)
        logger.info("SHA256 hash of the PDF file: %s", sha256_hash)
        
        certificates_obj = Certificates.objects.filter(certificate_hash=sha256_hash).first()
        if not certificates_obj or certificates_obj.is_parsed:
            logger.info("No certificates found or already parsed.")
            return None
        
        extracted_texts = extract_text(file_path)
        logger.info("Extracted text from PDF: %s", extracted_texts)
    
        if extracted_texts:
            student_id = extract_student_id(extracted_texts[4])
            student_name = extracted_texts[10]
            student_grade = extracted_texts[7].split()[1].strip('“”') if len(extracted_texts) > 7 else None
            student_sem = re.sub(r'\D', '', extracted_texts[8].split()[0] if len(extracted_texts) > 8 else None)
            student_certificate_issued_date = datetime.strptime(extracted_texts[12], "%B %d, %Y").date()
            student_course_completion_date = datetime.strptime(extracted_texts[13], "%B %d, %Y").date()
            certificate_id = extracted_texts[11] if len(extracted_texts) > 11 else None
            degree_name, department_name = extract_department_degree_names(extracted_texts[6])
            certificate_type = extracted_texts[9]
            course_name = extract_course_name(extracted_texts[5])
            
            student_dict = {}
            if student_id or student_name:
                student_dict["enrollment_no"] = student_id
                student_dict["student_name"] = student_name
                student_obj = Student.objects.create(**student_dict)
                certificates_obj.student_id = student_obj.pk
            else:
                student_obj = Student.objects.create()
                certificates_obj.student_id = student_obj.pk
                
            
            if any([student_grade, student_sem, student_certificate_issued_date, student_course_completion_date]):
                student_marks_data = {
                    "semester": student_sem,
                    "grade": student_grade,
                    "certificate_issued_date": student_certificate_issued_date,
                    "certificate_completion_date": student_course_completion_date,
                    "student_id": student_obj.pk
                }
                student_marks_obj = StudentMarks.objects.create(**student_marks_data)
                
                
            if certificate_type:
                certificate_type_obj, _ = Certificatetype.objects.get_or_create(certificate_name=certificate_type)
                certificates_obj.certificatetype = certificate_type_obj
            
            if course_name:
                course_obj, _ = Course.objects.get_or_create(course_name=course_name)
                certificates_obj.course = course_obj
            
            if degree_name:
                degree_obj, _ = Degree.objects.get_or_create(degree_name=degree_name)
            
            if department_name:
                if degree_obj:
                    department_obj, _= Department.objects.get_or_create(department_name=department_name,degree=degree_obj)
                else:
                    department_obj, _= Department.objects.get_or_create(department_name=department_name)
                certificates_obj.department = department_obj
            
            certificates_obj.certificate_id=certificate_id
            certificates_obj.is_parsed = True
            certificates_obj.save()
            logger.info("Certificate data extraction completed successfully.")
            return {"Result": "success"}
    except Exception as e:
        logger.error("Error occurred during certificate data extraction: %s", e)
        return e