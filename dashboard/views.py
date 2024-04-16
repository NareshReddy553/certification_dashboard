import random
from rest_framework import views, status
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils.timezone import now
import os
from django.db import transaction

# Create your views here.
from rest_framework.decorators import api_view
from django.db.models import Count, Case, When, IntegerField
from django.db.models.functions import ExtractWeekDay, ExtractMonth
from config.settings import WATCH_FOLDER_PATH
from dashboard.data_parsing import certificate_data_extraction_from_pdf
from dashboard.generate_certificate import pdf_creation
from dashboard.models import Certificates, Configurations, Users

from dashboard.serializers import FileUploadSerializer, UsersSerializer
import zipfile
from io import BytesIO
from faker import Faker


@api_view(["GET"])
def get_clients_ws_deptartments(request):
    queryset = Users.objects.all()
    serializer = UsersSerializer(queryset, many=True)
    if serializer.data:
        return Response(serializer.data)
    return None
    

@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def dashBoard_data(request):
    inputdata = request.data
    filters,data = {},{}

    # Add 'dept_id' filter if present
    if inputdata.get("department_id"):
        filters['department_id'] = inputdata.get("department_id")

    # Add 'client_id' filter if present
    if inputdata.get("issuer_id"):
        filters['user_id'] = inputdata.get("issuer_id")

    # Apply filters to the queryset
    queryset = Certificates.objects.filter(**filters)

    total_certificates_generated = queryset.distinct().count()
    active_users_count = queryset.filter(is_active=True).annotate(user_count=Count('user', distinct=True)).values('user_count').distinct().count()
    users_certificate_verified_count = queryset.filter(is_verified=True).distinct().count()
    
    data['total_certificates_generated']=total_certificates_generated
    data['active_users_count']=active_users_count
    data['users_certificate_verified_count']=users_certificate_verified_count
    
    return Response(data)


@api_view(["PUT"])
def dashboard_chart_data(request):
    
    inputdata =request.data  # Example inputdata

    filters = {}

    # Add 'dept_id' filter if present
    if inputdata.get("department_id"):
        filters['department_id'] = inputdata.get("department_id")

    # Add 'client_id' filter if present
    if inputdata.get("issuer_id"):
        filters['user_id'] = inputdata.get("issuer_id")

    # Apply filters to the queryset
    objects = Certificates.objects.filter(**filters)
    
    day_map = {
            1: 'Mon',
            2: 'Tue',
            3: 'Wed',
            4: 'Thu',
            5: 'Fri',
            6: 'Sat',
            7: 'Sun'
        }

    # Define a mapping from month number to month name
    month_map = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }

    # Initialize weekly data with zero counts for all days of the week
    weekly_data = [{'day': day, 'count': 0, 'verified_users': 0} for day in day_map.values()]

    # Initialize monthly data with zero counts for all months
    monthly_data = [{'month': month, 'count': 0, 'verified_users': 0} for month in month_map.values()]


    # Calculate weekly statistics
    weekly_counts = (
        objects.annotate(day_of_week=ExtractWeekDay('created_at'))
                .values('day_of_week')
                .annotate(
                    count=Count('id'),
                    verified_users=Count(Case(When(is_verified=True, then=1), output_field=IntegerField()))
                )
    )

    # Update weekly_data with counts from the database query
    for entry in weekly_counts:
        day = day_map.get(entry['day_of_week'])
        count = entry['count']
        verified_users = entry['verified_users']
        weekly_data[next(index for index, day_data in enumerate(weekly_data) if day_data['day'] == day)] = {
            'day': day,
            'count': count,
            'verified_users': verified_users
        }

    # Calculate monthly statistics
    monthly_counts = (
        objects.annotate(month=ExtractMonth('created_at'))
                .values('month')
                .annotate(
                    count=Count('id'),
                    verified_users=Count(Case(When(is_verified=True, then=1), output_field=IntegerField()))
                )
    )

    # Update monthly_data with counts from the database query
    for entry in monthly_counts:
        month = month_map.get(entry['month'])
        count = entry['count']
        verified_users = entry['verified_users']
        monthly_data[next(index for index, month_data in enumerate(monthly_data) if month_data['month'] == month)] = {
            'month': month,
            'count': count,
            'verified_users': verified_users
        }

    return Response({'weekly': weekly_data, 'monthly': monthly_data})

@transaction.atomic
@api_view(['GET'])
def certificate_data_parsing(request):
# def certificate_data_parsing(folder_path):
#     print(folder_path)
    try:
        folder_path = Configurations.objects.filter(data_key='windowsdestpath').first()
        if not folder_path or not os.path.exists(folder_path.data_value):
            return Response("Folder path does not exist.")
        WATCH_FOLDER_PATH = folder_path.data_value
        for filename in os.listdir(WATCH_FOLDER_PATH):
            file_path = os.path.join("C:\\Users\\ADMIN\\Desktop\\watch_folder", "Aaron Giles_issue.pdf")
            certificate_data_extraction_from_pdf(file_path)
        
        return Response({"message": "Certificate data parsing successful."})
    
    except Exception as e:
        return Response(e)
    
    
@api_view(["GET"])
def generate_certificate_view(request):
    fake = Faker()
    input_data = {  "university":["Massachusetts Institute of Technology (MIT)","Harvard University","Stanford University","University of California Berkeley (UCB)","University of Chicago","University of Pennsylvania","Cornell University","California Institute of Technology (Caltech)","Yale University","Princeton University","Columbia University","Johns Hopkins University","University of California, Los Angeles (UCLA)","University of Michigan-Ann Arbor","New York University (NYU)","Northwestern University","Carnegie Mellon University","Duke University","University of Texas at Austin","University of California, San Diego (UCSD)","University of Washington","University of Illinois at Urbana-Champaign","Brown University","Pennsylvania State University","Boston University"],
                    "department":["Department of Computer Science","Department of Electrical Engineering","Department of Mechanical Engineering","Department of Civil Engineering","Department of Chemical Engineering","Department of Aerospace Engineering","Department of Biomedical Engineering","Department of Industrial Engineering","Department of Software Engineering","Department of Information Technology","Department of Mathematics","Department of Physics","Department of Chemistry","Department of Biology","Department of Environmental Science","Department of Earth Sciences","Department of Psychology","Department of Sociology","Department of Economics","Department of Political Science","Department of History","Department of English","Department of Foreign Languages","Department of Linguistics","Department of Philosophy","Department of Business Administration","Department of Finance","Department of Marketing","Department of Operations Management","Department of Human Resource Management","Department of Accounting","Department of Law","Department of Medicine","Department of Nursing","Department of Pharmacy","Department of Dentistry","Department of Public Health","Department of Social Work","Department of Education","Department of Fine Arts","Department of Music","Department of Theatre Arts","Department of Film Studies","Department of Journalism","Department of Communication","Department of Library Science","Department of Physical Education","Department of Nutrition and Dietetics","Department of Agriculture","Department of Veterinary Science"],
                    "degree":["Bachelor of Arts (BA)","Bachelor of Science (BS/BSc)","Bachelor of Fine Arts (BFA)","Bachelor of Business Administration (BBA)","Bachelor of Engineering (BEng)","Bachelor of Laws (LLB)","Bachelor of Education (BEd)","Bachelor of Music (BMus)","Bachelor of Architecture (BArch)","Bachelor of Nursing (BN)","Bachelor of Social Work (BSW)","Bachelor of Commerce (BCom)","Bachelor of Technology (BTech)","Bachelor of Philosophy (BPhil)","Master of Arts (MA)","Master of Science (MS/MSc)","Master of Business Administration (MBA)","Master of Fine Arts (MFA)","Master of Engineering (MEng)","Master of Laws (LLM)","Master of Education (MEd)","Master of Music (MMus)","Master of Architecture (MArch)","Master of Social Work (MSW)","Master of Commerce (MCom)","Master of Technology (MTech)","Master of Philosophy (MPhil)","Doctor of Philosophy (PhD)","Doctor of Medicine (MD)","Doctor of Education (EdD)","Doctor of Business Administration (DBA)","Doctor of Engineering (EngD)","Doctor of Psychology (PsyD)","Doctor of Nursing Practice (DNP)","Doctor of Jurisprudence (JD)","Doctor of Dental Surgery (DDS)","Doctor of Veterinary Medicine (DVM)","Juris Doctor (JD)","Doctor of Medicine (MD)","Doctor of Dental Surgery (DDS)","Doctor of Pharmacy (PharmD)","Doctor of Optometry (OD)","Doctor of Physical Therapy (DPT)","Doctor of Occupational Therapy (OTD)","Doctor of Chiropractic (DC)","Doctor of Podiatric Medicine (DPM)","Associate of Arts (AA)","Associate of Science (AS)","Associate of Applied Science (AAS)","Associate of Business Administration (ABA)","Associate of Engineering (AEng)","Associate of Arts in Teaching (AAT)","Associate of Nursing (AN)","Associate of Occupational Studies (AOS)"],
                    "course":["Computer Science Fundamentals","Data Structures and Algorithms","Software Engineering","Artificial Intelligence","Machine Learning","Cybersecurity","Database Management","Computer Networks","Accounting","Marketing","Finance","Operations Management","Human Resource Management","Business Analytics","Entrepreneurship","Strategic Management","Electrical Engineering","Mechanical Engineering","Civil Engineering","Aerospace Engineering","Chemical Engineering","Environmental Engineering","Biomedical Engineering","Industrial Engineering"],
                    "type":["Course completion certificate", "specialization certificate", "Overall Degree Certifcate"]
                }

    required_fields = {
        'university': 'university',
        'department': 'department',
        'degree': 'degree',
        'course':'course',
        'type': 'type',
    }

    error = {field_key: f'{field_name} is required in the payload' for field_key, field_name in required_fields.items() if not input_data.get(field_key)}
    if error:
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    # Extract data from input
    # names = input_data['names']
    university = input_data['university']
    department = input_data['department']
    degree = input_data['degree']
    course = input_data.get('course')  # Optional
    type = input_data['type']

   
    # filename=random.choice(names)
    # pdf_content=pdf_creation(filename, random.choice(university), random.choice(course), random.choice(department), random.choice(degree), random.choice(type))
    
    # response = HttpResponse(pdf_content, content_type='application/pdf')
    # response['Content-Disposition'] = "attachment; filename=%s" % filename
    # return response
    
    pdfs_buffer = BytesIO()
    with zipfile.ZipFile(pdfs_buffer, 'w') as zip_file:
        for _ in range(10):  # Generate 10 PDFs
            filename = fake.name()
            pdf_content = pdf_creation(filename, random.choice(university), random.choice(course), random.choice(department), random.choice(degree), random.choice(type))
            zip_file.writestr(f'{filename}.pdf', pdf_content)

    # Prepare the response with the zip archive
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'inline; filename="certificates.zip"'
    pdfs_buffer.seek(0)
    response.write(pdfs_buffer.getvalue())

    return response


class ExtractPDFContentView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['file']
            try:
                certificate_data_extraction_from_pdf(pdf_file)

                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)