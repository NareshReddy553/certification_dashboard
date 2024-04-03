from django.core.cache import cache

from dashboard.models import Certificatetype, Course, Degree, Department, Users

def get_cached_user(userid):
    if userid is None:
        return None
    user = cache.get("USER_" + str(userid))
    if user is None:
        user = Users.objects.values(
            "id", "full_name", "is_active"
        ).get(pk=userid)
        if user is not None:
            cache.set("USER_" + str(userid), user, 120)
    return user

def get_cached_course(courseid):
    if courseid is None:
        return None
    course = cache.get("COURSE_" + str(courseid))
    if course is None:
        course = Course.objects.values(
            "course_id", "course_name"
        ).get(pk=courseid)
        if course is not None:
            cache.set("COURSE_" + str(courseid), course, 120)
    return course

def get_cached_degree(degreeid):
    if degreeid is None:
        return None
    degree = cache.get("DEGREE_" + str(degreeid))
    if degree is None:
        degree = Degree.objects.values(
            "degree_id", "degree_name"
        ).get(pk=degreeid)
        if degree is not None:
            cache.set("DEGREE_" + str(degreeid), degree, 120)
    return degree

def get_cached_department(departmentid):
    if departmentid is None:
        return None
    dept = cache.get("DEPT_" + str(departmentid))
    if dept is None:
        dept = Department.objects.values(
            "department_id", "department_name"
        ).get(pk=departmentid)
        if dept is not None:
            cache.set("DEPT_" + str(departmentid), dept, 120)
    return dept

def get_cached_certificatetype(certificatetypeid):
    if certificatetypeid is None:
        return None
    certificatetype = cache.get("CRTTYPE_" + str(certificatetypeid))
    if certificatetype is None:
        certificatetype = Certificatetype.objects.values(
            "certificatetype_id", "certificate_name"
        ).get(pk=certificatetypeid)
        if certificatetype is not None:
            cache.set("CRTTYPE_" + str(certificatetypeid), certificatetype, 120)
    return certificatetype