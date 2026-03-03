from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def admin_agreement(request): #view to render admin agreement
    return render(request, 'admin_agreement.html')

def recipient_agreement(request): #view to render recipient agreement
    return render(request, 'recipient_agreement.html')

def w9_upload(request): #view to render w9 upload page
    return render(request, 'w9_upload.html')