from django.urls import path
from . import views


urlpatterns = [
    path('recipient_agreement/', views.recipient_agreement, name='recipient_agreement'),
    path('w9_upload/', views.w9_upload, name='w9_upload'),
]