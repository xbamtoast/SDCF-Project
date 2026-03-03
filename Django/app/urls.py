from django.urls import path
from . import views


urlpatterns = [
    path('admin_agreement/', views.admin_agreement, name='admin_agreement'),
    path('recipient_agreement/', views.recipient_agreement, name='recipient_agreement'),
    path('w9_upload/', views.w9_upload, name='w9_upload'),
]