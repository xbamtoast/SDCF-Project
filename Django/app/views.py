from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MidYearReportForm, HopeGrantApplicationForm, EndYearReportForm

# Home/landing page view

def home(request):
    return render(request, 'landing.html')

def landing_page(request):
    return render(request, 'landing.html')

def recipient_agreement(request): #view to render recipient agreement
    return render(request, 'recipient_agreement.html')

def w9_upload(request): #view to render w9 upload page
    return render(request, 'w9_upload.html')

def hope_grant_application(request):
    if request.method == "POST":
        form = HopeGrantApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing")
    else:
        form = HopeGrantApplicationForm()
    return render(request, "application_and_reports/application.html", {"form":form})

# Mid year report view
def mid_year_report(request):
    if request.method == "POST":
        form = MidYearReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing")
    else:
        form = MidYearReportForm()

    return render(request, "application_and_reports/midyear_report.html", {"form": form})

def end_year_report(request):
    if request.method == "POST":
        form = EndYearReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing_page")
    else:
        form = EndYearReportForm()
    return render(request, "application_and_reports/endofyear_report.html", {"form": form})