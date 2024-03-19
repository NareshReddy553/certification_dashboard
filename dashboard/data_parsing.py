import re
import fitz

from dashboard.models import Certificates
from dashboard.util import calculate_sha256, extract_certificate_id, extract_course_name, extract_department_degree_names, extract_student_id
from datetime import datetime
from django.db import transaction
from dashboard.models import Certificates, Certificatetype, Course, Degree, Department, Student, StudentMarks

from dashboard.util import calculate_sha256



def extract_text(file_path):
    pdf_document = fitz.open(file_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_text = page.get_text()

        lines = page_text.split('\n')
        return lines
    
# @transaction.atomic
def certificate_data_extraction_from_pdf(file_path):
    try:
        
        sha256_hash = calculate_sha256(file_path)
        print("in side extraction")
        print(sha256_hash)
        print('--------------')
        certificates_obj = Certificates.objects.filter(certificate_hash=sha256_hash).first()
        if not certificates_obj or certificates_obj.is_parsed:
            return None
        extracted_texts=extract_text(file_path)
        print(extracted_texts)
    
        if extracted_texts:
            student_id=extract_student_id(extracted_texts[0])
            student_name = extracted_texts[10]
            student_grade = extracted_texts[12].split()[1].strip('“”')
            student_sem = re.sub(r'\D', '',extracted_texts[4].split()[0])
            student_certificate_issued_date = datetime.strptime(extracted_texts[6], "%B %d, %Y").date()
            student_course_completion_date = datetime.strptime(extracted_texts[8], "%B %d, %Y").date()
            certificate_id=extract_certificate_id(extracted_texts[2])
            degree_name,department_name=extract_department_degree_names(extracted_texts[3])
            certificate_type=extracted_texts[5]
            course_name=extract_course_name(extracted_texts[1])
            
            student_dict = {}
            if student_id or student_name:
                student_dict["enrollment_no"] = student_id
                student_dict["student_name"] = student_name
                student_obj = Student.objects.create(**student_dict)
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
            return {"Result":"sucess"}
    except Exception as e:
        print(e)
        return e    
        