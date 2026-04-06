from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import HopeGrantApplicationForm, MidYearReportForm, EndYearReportForm, ApplicationCommentForm, MidYearCommentForm, EndYearCommentForm, DocumentFormTest
from .models import HopeGrantApplication, MidYearReport, EndYearReport, ApplicationComment, MidYearComment, EndYearComment
from django.contrib import messages

from .models import HopeGrantApplication, MidYearReport, EndYearReport, ApplicationComment, MidYearComment, EndYearComment
from .models import Form, Question, Submission, Answer, SchoolDistrict
from .forms import SubmissionForm, build_answer_form

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

def dynamic_form(request, form_id):
    
    form_obj = get_object_or_404(Form, id=form_id)
    questions = Question.objects.filter(form=form_obj)

    if request.method == 'POST':
        submission_form = SubmissionForm(request.POST)
        answer_form = build_answer_form(questions, request.POST)

        if submission_form.is_valid() and answer_form.is_valid():
            submission = submission_form.save(commit=False)
            submission.submitted_by = request.user
            submission.form = form_obj
            submission.save()

            for question in questions:
                Answer.objects.create(
                    submission=submission,
                    question=question,
                    answer_text=answer_form.cleaned_data.get(f'question_{question.id}', '')
                )
            return redirect('home')
    else:
        submission_form = SubmissionForm()
        answer_form = build_answer_form(questions, data = None, filled_in = False, answer_texts = [])

    return render(request, 'application_and_reports/dynamic_form.html', {
        'form_obj': form_obj,
        'submission_form': submission_form,
        'answer_form': answer_form,
    })

def dynamic_form_detail(request, form_id, submission_id):

    # Read in the Form object.

    form_obj = get_object_or_404(Form, id = form_id)

    # Read in the Submission object.
    
    submission = get_object_or_404(Submission, id = submission_id)
    submission_form = SubmissionForm(instance = submission)

    # Read in the Answer objects.

    questions = Question.objects.filter(form = form_obj)
    answers = Answer.objects.filter(submission_id = submission_id)

    answer_texts = []
    for i in answers:
        answer_texts.append(i.answer_text)

    answer_form = build_answer_form(questions, data = None, filled_in = True,  answer_texts = answer_texts)
    
    context = {'form_obj':form_obj, 'submission':submission, 'submission_form':submission_form, 'answer_form':answer_form}

    return render(request, 'application_and_reports_detail/dynamic_form_detail.html', context = context)