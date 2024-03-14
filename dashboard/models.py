# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models


# class AdonisSchema(models.Model):
#     name = models.CharField(max_length=255)
#     batch = models.IntegerField()
#     migration_time = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'adonis_schema'


# class AdonisSchemaVersions(models.Model):
#     version = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'adonis_schema_versions'


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)
        
# class Clients(models.Model):
#     client_id = models.BigAutoField(primary_key=True)
#     client_name = models.CharField(unique=True, max_length=100)
#     is_active = models.BooleanField(default=True)
#     created_user = models.IntegerField(blank=True, null=True)
#     modified_user = models.IntegerField(blank=True, null=True)
#     created_datetime = models.DateTimeField(blank=True, null=True)
#     modified_datetime = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'clients'

# class Departments(models.Model):
#     dept_id = models.BigAutoField(primary_key=True)
#     dept_name = models.CharField(max_length=100, blank=True, null=True)
#     client = models.ForeignKey(Clients, on_delete=models.DO_NOTHING , related_name="departments")
#     is_active = models.IntegerField(blank=True, null=True)
#     created_datetime = models.DateTimeField(blank=True, null=True)
#     modified_datetime = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'departments'
        


# class Certificates(models.Model):
#     id=models.IntegerField(primary_key=True)
#     issuer_id = models.IntegerField()
#     certificate_hash = models.CharField(max_length=255)
#     tx_hash = models.CharField(max_length=255)
#     certificate_url = models.CharField(max_length=1000)
#     is_revoked = models.IntegerField()
#     revoked_by = models.IntegerField()
#     revoked_on = models.DateTimeField(blank=True, null=True)
#     is_active = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(blank=True, null=True)
#     is_verified = models.IntegerField(blank=True, null=True)
#     client = models.ForeignKey(Clients, on_delete=models.DO_NOTHING)
#     dept = models.ForeignKey(Departments, on_delete=models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'certificates'


# class Configurations(models.Model):
#     data_key = models.CharField(max_length=80, blank=True, null=True)
#     data_value = models.CharField(max_length=80, blank=True, null=True)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'configurations'
        


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'


# class EmailTemplates(models.Model):
#     template_slug = models.CharField(max_length=500)
#     template_name = models.CharField(max_length=255)
#     template_subject = models.TextField()
#     template_from = models.CharField(max_length=255)
#     template_from_mail = models.CharField(max_length=255)
#     template_html = models.TextField()
#     template_variables = models.CharField(max_length=500, db_comment='~ Separated')
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'email_templates'


# class Roles(models.Model):
#     slug = models.CharField(unique=True, max_length=255)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'roles'


# class Tokens(models.Model):
#     user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
#     name = models.CharField(max_length=255)
#     type = models.CharField(max_length=255)
#     token = models.CharField(unique=True, max_length=64)
#     expires_at = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'tokens'


# class UserRoles(models.Model):
#     role_id = models.IntegerField()
#     user_id = models.IntegerField()
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'user_roles'


# class Users(models.Model):
#     email = models.CharField(unique=True, max_length=255)
#     full_name = models.CharField(max_length=150, blank=True, null=True)
#     password = models.CharField(max_length=500, blank=True, null=True)
#     profile_picture = models.CharField(max_length=500, blank=True, null=True)
#     email_verified_at = models.DateTimeField(blank=True, null=True, db_comment='Default -> null')
#     is_revoked = models.IntegerField()
#     revoked_on = models.DateTimeField(blank=True, null=True)
#     revoked_by = models.IntegerField()
#     is_active = models.IntegerField(blank=True, null=True, db_comment='0- Inactive, 1- Active')
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'users'



        
# class File(models.Model):
#     name = models.CharField(primary_key=True, max_length=250)
#     hash = models.CharField(max_length=256, blank=True, null=True)
#     is_active = models.BooleanField(default=True,blank=True, null=True)
#     created_datetime = models.DateTimeField(blank=True, null=True)
#     modified_datetime = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'file'
        
        
        
#############################################################################################################
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdonisSchema(models.Model):
    name = models.CharField(max_length=255)
    batch = models.IntegerField()
    migration_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adonis_schema'


class AdonisSchemaVersions(models.Model):
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'adonis_schema_versions'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CertificateData(models.Model):
    certificate_data_id = models.AutoField(primary_key=True)
    certificate_id = models.IntegerField(unique=True)
    course_id = models.IntegerField(blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)
    degree_id = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificate data'


class Certificatetype(models.Model):
    certificatetype_id = models.AutoField(primary_key=True)
    certificate_name = models.CharField(unique=True, max_length=100)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'certificateType'


class Certificates(models.Model):
    id=models.BigAutoField(primary_key=True)
    issuer_id = models.IntegerField()
    certificate_hash = models.CharField(max_length=255)
    tx_hash = models.CharField(max_length=255)
    certificate_url = models.CharField(max_length=1000)
    is_revoked = models.IntegerField()
    revoked_by = models.IntegerField()
    revoked_on = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    is_parsed=models.BooleanField(default=False)
    student_id=models.IntegerField(blank=True, null=True)
    certificatetype_id=models.IntegerField(blank=True, null=True)
    degree_id=models.IntegerField(blank=True, null=True)
    course_id=models.IntegerField(blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'certificates'


class Clients(models.Model):
    client_id = models.BigAutoField(primary_key=True)
    client_name = models.CharField(unique=True, max_length=100)
    is_active = models.IntegerField(blank=True, null=True)
    created_user = models.IntegerField(blank=True, null=True)
    modified_user = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class Configurations(models.Model):
    data_key = models.CharField(max_length=80, blank=True, null=True)
    data_value = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configurations'


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(unique=True, max_length=100)
    user_id= models.IntegerField(blank=True, null=True)
    created_datetiem = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class Degree(models.Model):
    degree_id = models.AutoField(primary_key=True)
    degree_name = models.CharField(unique=True, max_length=100)
    user_id = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'degree'


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    degree_id = models.CharField(max_length=100, blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datatime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EmailTemplates(models.Model):
    template_slug = models.CharField(max_length=500)
    template_name = models.CharField(max_length=255)
    template_subject = models.TextField()
    template_from = models.CharField(max_length=255)
    template_from_mail = models.CharField(max_length=255)
    template_html = models.TextField()
    template_variables = models.CharField(max_length=500, db_comment='~ Separated')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_templates'


class Roles(models.Model):
    slug = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'roles'


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100, blank=True, null=True)
    enrollment_no = models.CharField(unique=True, max_length=100)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class StudentMarks(models.Model):
    studentmarks_id = models.AutoField(primary_key=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=1, blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)
    certificate_issued_date=models.DateField(blank=True, null=True)
    certificate_completion_date=models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_marks'


class Tokens(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'


class UserRoles(models.Model):
    role_id = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_roles'


class Users(models.Model):
    email = models.CharField(unique=True, max_length=255)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    profile_picture = models.CharField(max_length=500, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True, db_comment='Default -> null')
    is_revoked = models.IntegerField()
    revoked_on = models.DateTimeField(blank=True, null=True)
    revoked_by = models.IntegerField()
    is_active = models.IntegerField(blank=True, null=True, db_comment='0- Inactive, 1- Active')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
