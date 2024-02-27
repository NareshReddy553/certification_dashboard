
from rest_framework import serializers

from dashboard.models import Certificates, Clients, Departments


class CertificationSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()

    class Meta:
        model = Certificates
        fields = '__all__'
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields =[ 'dept_no','dept_name','is_active']

class ClientsSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Clients
        fields=['client_id', 'client_name', 'is_active', 'departments']