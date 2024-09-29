from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SendOtpView, VerifyOtpView, PublicUserLandingPageView, Get_live_time, UserRegistrationView, UserLogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Get_live_time.as_view(), name='get_live_time'), # delete this line 
    path('send-otp/', SendOtpView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('user_dashboard/', PublicUserLandingPageView.as_view(), name='user_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from .views import (
    StaffUserLoginView,
    StaffReportListView,
    ReportDetailAPIView,
    UpdateReportStatusAPIView,
    CreateReportAPIView
)

urlpatterns += [
    path('staff/signup/', UserRegistrationView.as_view(), name='User_registration'),
    path('staff/login/', StaffUserLoginView.as_view(), name='staff_login'),
    path('staff/reports/', StaffReportListView.as_view(), name='staff_reports'),
    path('staff/reports/<str:report_id>/', ReportDetailAPIView.as_view(), name='report_detail'),
    path('staff/reports/update-status/<str:report_id>/', UpdateReportStatusAPIView.as_view(), name='update_report_status'),
    path('staff/reports/create/', CreateReportAPIView.as_view(), name='create_report'),
]

urlpatterns += [
    path('logout/', UserLogoutView.as_view(), name='logout'),
]