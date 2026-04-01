from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import HopeGrantApplicationForm, MidYearReportForm, EndYearReportForm, ApplicationCommentForm, MidYearCommentForm, EndYearCommentForm, DocumentFormTest
from .models import HopeGrantApplication, MidYearReport, EndYearReport, ApplicationComment, MidYearComment, EndYearComment
from django.contrib import messages

# Home/landing page view

def home(request):
    return render(request, 'landing.html')

def landing_page(request):
    return render(request, 'landing.html')

def w9_upload(request):
    if request.method == 'POST':
        form = DocumentFormTest(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            print('Success')
            return redirect('app:home')
        else:
            print(form.errors)
    else:
        form = DocumentFormTest()
    return render(request, 'miscellaneous/w9_upload.html', {'form': form})

# Blank Hope Grant Application View

def hope_grant_application(request):

    if request.method == "POST":
        form = HopeGrantApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:home")
    else:
        form = HopeGrantApplicationForm()
    return render(request, "application_and_reports/application.html", {"form":form})

# Blank Mid-Year Application View

def mid_year_report(request):
    if request.method == "POST":
        form = MidYearReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:home")
    else:
        form = MidYearReportForm()

    return render(request, "application_and_reports/midyear_report.html", {"form": form})

# Blank Recipient Agreement View

def recipient_agreement(request): #view to render recipient agreement
    return render(request, 'application_and_reports/recipient_agreement.html')

# Blank End-Year Report View

def end_year_report(request):
    if request.method == "POST":
        form = EndYearReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:home")
    else:
        form = EndYearReportForm()
    return render(request, "application_and_reports/endyear_report.html", {"form": form})

def application_detail(request, pk):

    comments = ApplicationComment.objects.filter(submission_id = pk)
    item = get_object_or_404(HopeGrantApplication, pk = pk)
    form = HopeGrantApplicationForm(instance = item)

    if request.method == "POST":
        commentform = ApplicationCommentForm(request.POST)
        if commentform.is_valid():
            instance = commentform.save(commit = False)
            instance.submission_id = pk
            instance.save()
            return redirect(f'/hope-grant-application/{pk}/#comment-section-down')

    else:
        commentform = ApplicationCommentForm()

    return render(request, 'application_and_reports_detail/application_detail.html', {'form':form, 'commentform':commentform, 'comments':comments})


def mid_year_report_detail(request, pk):

    comments = MidYearComment.objects.filter(submission_id = pk)
    item = get_object_or_404(MidYearReport, pk = pk)
    form = MidYearReportForm(instance = item)

    if request.method == "POST":
        commentform = MidYearCommentForm(request.POST)
        if commentform.is_valid():
            instance = commentform.save(commit = False)
            instance.submission_id = pk
            instance.save()
            return redirect(f'/mid-year-report/{pk}/#comment-section-down')

    else:
        commentform = MidYearCommentForm()

    return render(request, 'application_and_reports_detail/midyear_report_detail.html', {'form':form, 'commentform':commentform, 'comments':comments})

def end_year_report_detail(request, pk):

    comments = EndYearComment.objects.filter(submission_id = pk)
    item = get_object_or_404(EndYearReport, pk = pk)
    form = EndYearReportForm(instance = item)

    if request.method == "POST":
        commentform = EndYearCommentForm(request.POST)
        if commentform.is_valid():
            instance = commentform.save(commit = False)
            instance.submission_id = pk
            instance.save()
            return redirect(f'/end-year-report/{pk}/#comment-section-down')
    else:
        commentform = EndYearCommentForm()

    return render(request, 'application_and_reports_detail/endyear_report_detail.html', {'form':form, 'commentform':commentform, 'comments':comments})