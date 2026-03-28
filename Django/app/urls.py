from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipient_agreement/', views.recipient_agreement, name='recipient_agreement'),
    path('w9_upload/', views.w9_upload, name='w9_upload'),
    path("hope-grant-application/", views.hope_grant_application, name="hope_grant_application"),
    path("mid-year-report/", views.mid_year_report, name="mid_year_report"),
    path("end-year-report/", views.end_year_report, name="end_year_report")
]