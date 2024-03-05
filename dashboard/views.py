import hashlib
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
# Create your views here.
from rest_framework.decorators import api_view
from django.db.models import Count, Case, When, IntegerField
from django.db.models.functions import ExtractWeekDay, ExtractMonth
from config.settings import WATCH_FOLDER_PATH

from dashboard.models import Certificates, Clients, File, Departments
from dashboard.serializers import ClientsSerializer
from dashboard.util import calculate_sha256, extract_text_by_coordinates, get_text_with_coordinates


@api_view(["GET"])
def get_clients_ws_deptartments(request):
    queryset = Clients.objects.all()
    serializer = ClientsSerializer(queryset, many=True)
    return Response(serializer.data)
    

@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def dashBoard_data(request):
    inputdata = request.data
    filters,data = {},{}

    # Add 'dept_id' filter if present
    if inputdata.get("dept_id"):
        filters['dept_id'] = inputdata.get("dept_id")

    # Add 'client_id' filter if present
    if inputdata.get("client_id"):
        filters['client_id'] = inputdata.get("client_id")

    # Apply filters to the queryset
    queryset = Certificates.objects.filter(**filters)

    # Perform further processing as needed
    total_certificates_generated = queryset.values('id').distinct().count()
    active_users_count = queryset.filter(is_active=True).values('id').distinct().count()
    users_certificate_verified_count = queryset.filter(is_verified=True).values('id').distinct().count()
    
    data['total_certificates_generated']=total_certificates_generated
    data['active_users_count']=active_users_count
    data['users_certificate_verified_count']=users_certificate_verified_count
    
    return Response(data)

@api_view(["PUT"])
def dashboard_chart_data(request):
    
    inputdata =request.data  # Example inputdata

    filters = {}

    # Add 'dept_id' filter if present
    if inputdata.get("dept_id"):
        filters['dept_id'] = inputdata.get("dept_id")

    # Add 'client_id' filter if present
    if inputdata.get("client_id"):
        filters['client_id'] = inputdata.get("client_id")

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


@api_view(['GET'])
def pdf_parsing_for_data(request):
    import os
    folder_path=WATCH_FOLDER_PATH
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return []
    
    processed_files = set(File.objects.filter(is_active=True).values_list('name', flat=True))

    for filename in os.listdir(WATCH_FOLDER_PATH):
        if filename not in processed_files:
            file_path = os.path.join(WATCH_FOLDER_PATH, filename)
            sha256_hash = calculate_sha256(file_path)
            Certificates_obj=Certificates.objects.filter(certificate_hash=sha256_hash).first()
            if Certificates_obj:
                x1, y1, x2, y2 = 468.9062,222.17653069999994,696.3088112,260.2438307  # Example coordinates
                extracted_text = extract_text_by_coordinates(file_path,x1, y1, x2, y2)
                if extracted_text:
                    dept_obj=Departments.objects.filter(dept_name=extracted_text).first()
                    Certificates_obj.dept_id=dept_obj.pk
                    Certificates_obj.client_id=dept_obj.client_id
                    Certificates_obj.save()
                    return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)