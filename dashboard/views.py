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
from dashboard.models import Certificates, Configurations, Users

from dashboard.serializers import UsersSerializer


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
    if inputdata.get("department_id"):
        filters['department_id'] = inputdata.get("department_id")

    # Add 'client_id' filter if present
    if inputdata.get("issuer_id"):
        filters['issuer_id'] = inputdata.get("issuer_id")

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
            file_path = os.path.join(WATCH_FOLDER_PATH, filename)
            certificate_data_extraction_from_pdf(file_path)
        
        return Response({"message": "Certificate data parsing successful."})
    
    except Exception as e:
        return Response(e)