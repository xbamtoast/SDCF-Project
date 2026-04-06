from django.urls import include, path
from . import views

app_name = 'app'

urlpatterns = [

    path('', views.home, name='home'),
    path('recipient_agreement/', views.recipient_agreement, name='recipient_agreement'),
    path('w9_upload/', views.w9_upload, name='w9_upload'),

    # Kinley Blank Forms to Submit

    path("hope-grant-application/", views.hope_grant_application, name="hope_grant_application"),
    path("recipient-agreement/", views.recipient_agreement, name="recipient_agreement"),
    path("mid-year-report/", views.mid_year_report, name="mid_year_report"),
    path("end-year-report/", views.end_year_report, name="end_year_report"),
    path("dynamic-form/<int:form_id>", views.dynamic_form, name="dynamic_form"),

    # This will send them to the individual view for each already submitted form.

    path("hope-grant-application/<int:pk>/", views.application_detail, name="application_detail"),
    path("mid-year-report/<int:pk>/", views.mid_year_report_detail, name="mid_year_report_detail"),
    path("end-year-report/<int:pk>/", views.end_year_report_detail, name="end_year_report_detail"),
    path("dynamic-form/<int:form_id>/<int:submission_id>", views.dynamic_form_detail, name="dynamic_form_detail"),

    # Applications Tables

    path("application_table_admin", views.application_table_admin, name="application_table_admin"),


]