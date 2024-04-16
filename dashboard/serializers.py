
from rest_framework import serializers

from dashboard.models import Certificates, Certificatetype, Course, Degree, Department, Student, StudentMarks, Users
from dashboard.service import get_cached_certificatetype, get_cached_course, get_cached_degree, get_cached_user

class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ['degree_id','degree_name']
        
class DepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields =[ 'department_id','department_name']
    
class DepartmentSerializer(serializers.ModelSerializer):
    degree=serializers.SerializerMethodField()
    
    def get_degree(self, obj):
        return get_cached_degree(obj.degree_id)
        
    class Meta:
        model = Department
        fields =[ 'department_id','department_name','degree']

class CertificatetypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Certificatetype
        fields=['certificatetype_id', 'certificate_name']
    
class UsersSerializer(serializers.ModelSerializer):
    departments=serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields=['id', 'full_name', 'departments']
    
    def get_departments(self, instance):
        try:
            certificates = Certificates.objects.filter(user=instance).prefetch_related('department')
            departments = [certificate.department for certificate in certificates if certificate.department_id]
            serialized_departments = DepartSerializer(departments, many=True).data 
            return serialized_departments
        except Certificates.DoesNotExist:
            return []

class StudentMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMarks
        fields = ['semester','grade','certificate_issued_date','certificate_completion_date']
class StudentSerializer(serializers.ModelSerializer):
    studentmarks = StudentMarksSerializer(many=True, read_only=True) 
    class Meta:
        model = Student
        fields = ['student_id','student_name','enrollment_no','studentmarks']         

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['course_id','course_name']   
        

        
class CertificateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'full_name']   
        

class CertificationSerializer(serializers.ModelSerializer):
    # user=CertificateUserSerializer(read_only=True)
    user = serializers.SerializerMethodField()

    
    student=StudentSerializer(read_only=True)
    # course=CourseSerializer(read_only=True)
    course=serializers.SerializerMethodField()
    # certificatetype=CertificatetypeSerializer(read_only=True)
    certificatetype=serializers.SerializerMethodField()
    department=DepartmentSerializer(read_only=True)
    
    def get_user(self, obj):
        return get_cached_user(obj.user_id)
    
    def get_course(self,obj):
        return get_cached_course(obj.course_id)
    
    def get_certificatetype(self,obj):
        return get_cached_certificatetype(obj.certificatetype_id)
    
    class Meta:
        model = Certificates
        fields = ['id','user','student','course','certificatetype','department','created_at','certificate_id']
        
        

        

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()