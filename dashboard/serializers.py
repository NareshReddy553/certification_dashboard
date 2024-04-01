
from rest_framework import serializers

from dashboard.models import Certificates, Certificatetype, Course, Degree, Department, Student, StudentMarks, Users

class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ['degree_id','degree_name']
class DepartmentSerializer(serializers.ModelSerializer):
    degree=DegreeSerializer(read_only=True)
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
            certificates =Certificates.objects.filter(user=instance)
            all_departments = []
            for certificate in certificates:
                if certificate.department_id:
                    all_departments.append(certificate.department)
            return DepartmentSerializer(all_departments, many=True).data
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
    user=CertificateUserSerializer(read_only=True)
    student=StudentSerializer(read_only=True)
    course=CourseSerializer(read_only=True)
    certificatetype=CertificatetypeSerializer(read_only=True)
    department=DepartmentSerializer(read_only=True)

    class Meta:
        model = Certificates
        fields = ['id','user','student','course','certificatetype','department','created_at','certificate_id']
        
        

        

