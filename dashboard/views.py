import hashlib
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils.timezone import now
from datetime import datetime, timedelta
import os
from django.db import transaction

# Create your views here.
from rest_framework.decorators import api_view
from django.db.models import Count, Case, When, IntegerField
from django.db.models.functions import ExtractWeekDay, ExtractMonth
from config.settings import WATCH_FOLDER_PATH
from dashboard.models import Certificates, Certificatetype, Configurations, Course, Degree, Department, Student, StudentMarks

# from dashboard.models import Certificates, Clients, File, Departments,Configurations
# from dashboard.serializers import ClientsSerializer
from dashboard.util import calculate_sha256, extract_text_by_coordinates, get_text_with_coordinates


@api_view(["GET"])
def get_clients_ws_deptartments(request):
    # queryset = Clients.objects.all()
    # serializer = ClientsSerializer(queryset, many=True)
    # return Response(serializer.data)
    return None
    

@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def dashBoard_data(request):
    # inputdata = request.data
    # filters,data = {},{}

    # # Add 'dept_id' filter if present
    # if inputdata.get("dept_id"):
    #     filters['dept_id'] = inputdata.get("dept_id")

    # # Add 'client_id' filter if present
    # if inputdata.get("client_id"):
    #     filters['client_id'] = inputdata.get("client_id")

    # # Apply filters to the queryset
    # queryset = Certificates.objects.filter(**filters)

    # # Perform further processing as needed
    # total_certificates_generated = queryset.values('id').distinct().count()
    # active_users_count = queryset.filter(is_active=True).values('id').distinct().count()
    # users_certificate_verified_count = queryset.filter(is_verified=True).values('id').distinct().count()
    
    # data['total_certificates_generated']=total_certificates_generated
    # data['active_users_count']=active_users_count
    # data['users_certificate_verified_count']=users_certificate_verified_count
    
    # return Response(data)
    return None

@api_view(["PUT"])
def dashboard_chart_data(request):
    
    # inputdata =request.data  # Example inputdata

    # filters = {}

    # # Add 'dept_id' filter if present
    # if inputdata.get("dept_id"):
    #     filters['dept_id'] = inputdata.get("dept_id")

    # # Add 'client_id' filter if present
    # if inputdata.get("client_id"):
    #     filters['client_id'] = inputdata.get("client_id")

    # # Apply filters to the queryset
    # objects = Certificates.objects.filter(**filters)
    
    # day_map = {
    #         1: 'Mon',
    #         2: 'Tue',
    #         3: 'Wed',
    #         4: 'Thu',
    #         5: 'Fri',
    #         6: 'Sat',
    #         7: 'Sun'
    #     }

    # # Define a mapping from month number to month name
    # month_map = {
    #     1: 'Jan',
    #     2: 'Feb',
    #     3: 'Mar',
    #     4: 'Apr',
    #     5: 'May',
    #     6: 'Jun',
    #     7: 'Jul',
    #     8: 'Aug',
    #     9: 'Sep',
    #     10: 'Oct',
    #     11: 'Nov',
    #     12: 'Dec'
    # }

    # # Initialize weekly data with zero counts for all days of the week
    # weekly_data = [{'day': day, 'count': 0, 'verified_users': 0} for day in day_map.values()]

    # # Initialize monthly data with zero counts for all months
    # monthly_data = [{'month': month, 'count': 0, 'verified_users': 0} for month in month_map.values()]


    # # Calculate weekly statistics
    # weekly_counts = (
    #     objects.annotate(day_of_week=ExtractWeekDay('created_at'))
    #             .values('day_of_week')
    #             .annotate(
    #                 count=Count('id'),
    #                 verified_users=Count(Case(When(is_verified=True, then=1), output_field=IntegerField()))
    #             )
    # )

    # # Update weekly_data with counts from the database query
    # for entry in weekly_counts:
    #     day = day_map.get(entry['day_of_week'])
    #     count = entry['count']
    #     verified_users = entry['verified_users']
    #     weekly_data[next(index for index, day_data in enumerate(weekly_data) if day_data['day'] == day)] = {
    #         'day': day,
    #         'count': count,
    #         'verified_users': verified_users
    #     }

    # # Calculate monthly statistics
    # monthly_counts = (
    #     objects.annotate(month=ExtractMonth('created_at'))
    #             .values('month')
    #             .annotate(
    #                 count=Count('id'),
    #                 verified_users=Count(Case(When(is_verified=True, then=1), output_field=IntegerField()))
    #             )
    # )

    # # Update monthly_data with counts from the database query
    # for entry in monthly_counts:
    #     month = month_map.get(entry['month'])
    #     count = entry['count']
    #     verified_users = entry['verified_users']
    #     monthly_data[next(index for index, month_data in enumerate(monthly_data) if month_data['month'] == month)] = {
    #         'month': month,
    #         'count': count,
    #         'verified_users': verified_users
    #     }

    # return Response({'weekly': weekly_data, 'monthly': monthly_data})
    return None

@transaction.atomic
@api_view(['GET'])
def certificate_data_parsing(request):
    
    coordinates_mapping = {
        "student_id":(401.72300000000007,305.38149999999996,440.09100000000007,317.38149999999996),
        "student_name":(330.5474, 229.30819999999994, 501.9974, 279.30819999999994),
        "course":(273.564208984375, 321.5094909667969, 425.32708740234375, 336.37750244140625),
        "degree":(220.81790161132812,347.8912353515625,412.796630859375,372.4127197265625),
        "department":(442.5177917480469,347.8912353515625,621.0965576171875,372.4127197265625),
        "certificate_type":(343.3118896484375, 420.02789306640625, 500.7439270019531,434.69189453125),
        "grade":(440.6475524902344,376.91070556640625,445.05255126953125, 395.4956970214844),
        "semester":(385.3359069824219,401.03192138671875,  390.08795166015625,415.6959228515625),
        "issued_date":(90.54389953613281,502.83990478515625, 174.20794677734375,517.263916015625),
        "completion_date":( 665.47021484375,501.38909912109375,762.1182861328125, 515.8131103515625)
        
        
        
        
        
        # Add more entities and their coordinates as needed
    }
    
    folder_path=Configurations.objects.filter(data_key='windowsdestpath').first()
    # folder_path=WATCH_FOLDER_PATH
    if folder_path:
        if  not os.path.exists(folder_path.data_value):
            print("Folder path does not exist.")
            return []
    
    # # processed_files = set(File.objects.filter(is_active=True).values_list('name', flat=True))
    WATCH_FOLDER_PATH=folder_path.data_value
    for filename in os.listdir(WATCH_FOLDER_PATH):
        file_path = os.path.join(WATCH_FOLDER_PATH, filename)
        sha256_hash = calculate_sha256(file_path)
        Certificates_obj=Certificates.objects.filter(certificate_hash=sha256_hash).first()
        if not Certificates_obj :
            continue
        elif Certificates_obj.is_parsed:
            continue
            
        extracted_texts = extract_text_by_coordinates(file_path,coordinates_mapping)
        get_text_with_coordinates(file_path, "123456")
        
        student_id = extracted_texts["student_id"]
        student_name = extracted_texts["student_name"]
        student_grade=extracted_texts["grade"]
        student_sem=extracted_texts["semester"]
        #TODO date parsing
        student_certificate_issued_date=extracted_texts["issued_date"]
        student_course_completion_date=extracted_texts["completion_date"]
        studentinfo={}
        student_dict={}
        
        if student_id:
            student_dict["enrollment_no"]=student_id
        if student_name:
            student_dict["student_name"]=student_name
            
            student_obj=Student(**student_dict)
            student_obj.save()
            Certificates_obj.student_id=student_obj.pk
            
        
        if student_grade or student_sem or student_certificate_issued_date or student_course_completion_date:
            
            studentinfo["semester"]=student_sem
            studentinfo["grade"]=student_grade
            studentinfo["certificate_issued_date"]=datetime.strptime(student_certificate_issued_date, "%B %d, %Y").date()
            studentinfo["certificate_completion_date"]=datetime.strptime(student_course_completion_date, "%B %d, %Y").date()
            studentinfo["student_id"]=student_obj.pk
            
            studentmarks_obj=StudentMarks.objects.create(**studentinfo)
            
            
            
            
            
        course=extracted_texts["course"]
        course_data={}
        if course:
            course_data["course_name"]=course
            course_data["user_id"]=Certificates_obj.issuer_id
            course_obj,_=Course.objects.get_or_create(**course_data)
            Certificates_obj.course_id=course_obj.pk
            
            
        
        degree=extracted_texts["degree"]
        degree_data={}
        if degree:
            degree_data["degree_name"]=degree
            degree_data["user_id"]=Certificates_obj.issuer_id
            degree_obj=Degree.objects.get_or_create(**degree_data)
            Certificates_obj.degree_id=degree_obj.pk
            
            
        department=extracted_texts["department"]
        department_data={}
        if department:
            department_data["department_name"]=department
            department_data["degree_id"]=Certificates_obj.degree_id
            department_obj=Department.objects.get_or_create(**department_data)
        
            
        certificate_type=extracted_texts["certificate_type"]
        if certificate_type:
            certificate_type_obj,_=Certificatetype.objects.get_or_create(certificate_name=certificate_type)
            # if certificate_type_obj:
            #     pass
            # else:
            #     certificate_type_data["certificate_name"]=certificate_type
            #     certificate_type_obj=Certificatetype.objects.create(**certificate_type_data)
            Certificates_obj.certificatetype_id=certificate_type_obj.pk
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    #     # if certificate is not parsed then we need to parse for the department
        
    #     # 1. Extract degree name and update certificate
        
        # extracted_texts = extract_text_by_coordinates(file_path,coordinates_mapping)
        # department_text = extracted_texts["department"]
        # if department_text:
        #     dept_obj=Department.objects.filter(dept_name=department_text).first()
        #     if dept_obj:
        #         Certificates_obj.dept_id=dept_obj.pk    
                
    #     student_id = extracted_texts["student_id"]
    #     student_name = extracted_texts["student_name"]
    #     if student_id and student_name:
    #         student_obj=Student.objects.filter(pk=student_id).first()
    #         if student_obj:
    #             Certificates_obj.student_id=student_obj.pk
    #             student_obj.student_name=student_name
    #             student_obj.save() 
    #         else:
    #             new_student_obj=Student.objects.create(pk=student_id,student_name=student_name)
    #             Certificates_obj.student_id=new_student_obj.pk
        
    #     course_text=extracted_texts["course"]
    #     if course_text:
    #         course_obj= Course.objects.filter(course_name=course_text).first()
    #         if course_obj:
    #             Certificates_obj.course_id=course_obj.pk
    #         else:
    #            new_course_obj=Course.objects.create(course_name=course_text)
    #            Certificates_obj.course_id=new_course_obj.pk
               
        
            
            
            
        
        
        
    #     if filename not in processed_files:
    #         file_path = os.path.join(WATCH_FOLDER_PATH, filename)
    #         sha256_hash = calculate_sha256(file_path)
    #         Certificates_obj=Certificates.objects.filter(certificate_hash=sha256_hash).first()
            
    #         if Certificates_obj:
    #             x1, y1, x2, y2 = 468.9062,222.17653069999994,696.3088112,260.2438307  # Example coordinates
    #             extracted_text = extract_text_by_coordinates(file_path,x1, y1, x2, y2)
    #             if extracted_text:
    #                 dept_obj=Departments.objects.filter(dept_name=extracted_text).first()
    #                 Certificates_obj.dept_id=dept_obj.pk
    #                 Certificates_obj.client_id=dept_obj.client_id
    #                 Certificates_obj.save()
    #                 return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)