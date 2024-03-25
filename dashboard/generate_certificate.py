
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors
import calendar
import random
import string
from io import BytesIO
import os

from config.settings import BASE_DIR
my_path="C:\\Users\\ADMIN\\Desktop\\watch_folder\\cert-2-1.pdf"

def generate_random_alphanumeric(length=10):
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def generate_random_grade():
    grades = ['A', 'B', 'C', 'D']
    random_grade = random.choice(grades)
    
    return random_grade

def generate_random_semester():
    semesters = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
    
    random_semester = random.choice(semesters)
    
    return random_semester

def generate_random_date():
    year = random.randint(2000, 2024)
    month = random.randint(1, 12)
    month_name = calendar.month_name[month]
    max_day = calendar.monthrange(year, month)[1]
    day = random.randint(1, max_day)
    random_date = f"{month_name} {day}, {year}"
    
    return random_date

def generate_two_random_dates():
    first_date = generate_random_date()
    second_date = generate_random_date()
    while second_date <= first_date:
        second_date = generate_random_date()
    
    return first_date, second_date

def pdf_creation(name,university,course,department,degree,type,dest_path):
    rel_path = os.path.join('media', 'static', 'cert-2-1.pdf')
    file_path = os.path.join(BASE_DIR, rel_path)
    name,university,course,department,degree,type,dest_path=name,university,course,department,degree,type,dest_path
    input_pdf = PdfReader(open(file_path, "rb"))
    output_pdf = PdfWriter()
    page = input_pdf.pages[0]
    page_media_box = page.mediabox
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(13*inch, 9.2*inch))
    width=13*inch
    height=9.2*inch
    top_edge = float(page_media_box[3])
    std_id=generate_random_alphanumeric(length=10)

    style = ParagraphStyle(name="Normal", fontName="Helvetica", fontSize=12,alignment=1,leading=20,textColor=colors.HexColor('#726658'))
    # p1=Paragraph('''This is to certify that <b>John Smith</b> (Student ID: <b>{std_id}</b>) has successfully completed the course titled<BR/>\
    #     <b>Introduction to Data Science</b> offered by <b>Pune University</b>.<BR/><BR/>\
    #         <font size="20" color="#221E1F">Bachelor of Science in Computer Science</font><BR/>\
    #             <font size="14" color="#221E1F"><b>Grade “B”</b></font><BR/>\
    #                 <font color="#9B8579"><b>2nd Semester<BR/>\
    #                 Course Completion Certificate</b></font> ''',style)
    grade=generate_random_grade()
    semester=generate_random_semester()
    text_template = '''This is to certify that <b>{name}</b> (Student ID: <b>{std_id}</b>) has successfully completed the course titled<BR/>\
        <b>{course}</b> offered by <b>{university}</b>.<BR/><BR/>\
            <font size="18" color="#221E1F">{degree} in {department}</font><BR/>\
                <font size="14" color="#221E1F"><b>Grade “{grade}”</b></font><BR/>\
                    <font color="#9B8579"><b>{semester} Semester<BR/>\
                    {type}</b></font> '''

    # Format the text with actual data

    text = text_template.format(name=name,std_id=std_id, course=course, university=university,
                                grade=grade, semester=semester,type=type,degree=degree,department=department)
    p1 = Paragraph(text, style)
    p1.wrap(c._pagesize[0], c._pagesize[1])
    paragraph_width = p1.width
    x_center = (c._pagesize[0] - paragraph_width) / 2
    p1.drawOn(c, x_center-50, 170)
    style1 = ParagraphStyle(name="Normal", fontName="Helvetica",alignment=1)
    text_template2='''<font size='22' >{name}</font>'''
    text2 = text_template2.format(name=name)
    p2=Paragraph(text2,style1)
    p2.wrap(c._pagesize[0], c._pagesize[1])
    paragraph_width = p2.width
    x_center = (c._pagesize[0] - paragraph_width) / 2
    p2.drawOn(c, x_center-50, 340)
    c.drawString(105, top_edge -37.5, generate_random_alphanumeric(length=10))
    date1,date2=generate_two_random_dates()
    c.drawString(87, top_edge -518, date2)
    c.drawString(700-49, top_edge -517, date1)
    c.showPage()
    c.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    new_page = new_pdf.pages[0]
    page.merge_page(new_page)
    output_pdf.add_page(page)
    if os.path.isdir(dest_path[0]):
        old=dest_path[0]+name+'.pdf'
        with open(old, "wb") as f:
            output_pdf.write(f)
    return None

