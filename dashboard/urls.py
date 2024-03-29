# from django.conf.urls import include, url
from django.urls import path, include
from rest_framework import routers
from dashboard.views import dashBoard_data, dashboard_chart_data, generate_certificate_view,get_clients_ws_deptartments,certificate_data_parsing

from dashboard.viewsets import CertificatesViewSet


router = routers.DefaultRouter()
router.register(r"certificates", CertificatesViewSet, basename="certification")

urlpatterns = [
    # path(r'userprofile', user_profile),
    # path("password/reset/", ResetPasswordRequestView.as_view()),
    # path("password/change/", ChangePasswordView.as_view()),
    path(r'dashBoard_data', dashBoard_data),
    path(r'dashBoard_chart_data', dashboard_chart_data),
    path(r'clients_departments',get_clients_ws_deptartments),
    path(r'watch_files',certificate_data_parsing),
    path(r'generate_cert',generate_certificate_view),
    path("", include(router.urls)),
]