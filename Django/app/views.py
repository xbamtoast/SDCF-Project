from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import DocumentFormTest
from django.contrib import messages

from .models import Form, Question, Submission, Answer, SchoolDistrict, Comment
from .forms import SubmissionForm, CommentForm, build_answer_form
from django.core.paginator import Paginator
from django.db.models import Q

from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

# Home/landing page view

def directory(request):
    return render(request, 'miscellaneous/directory.html')

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

# Blank Recipient Agreement View

def recipient_agreement(request): #view to render recipient agreement
    return render(request, 'application_and_reports/recipient_agreement.html')

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
            return redirect('app:home')
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

    if (submission.submitted_by != request.user.username) and ((request.user.is_staff == False) and (request.user.is_superuser == False)):
        return render(request, 'miscellaneous/permission_denied.html', context = {})

    # Read in the Answer objects.

    questions = Question.objects.filter(form = form_obj)
    answers = Answer.objects.filter(submission_id = submission_id)

    comments = Comment.objects.filter(form_id = form_id, submission_id = submission_id)
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    answer_texts = []
    for i in answers:
        answer_texts.append(i.answer_text)

    answer_form = build_answer_form(questions, data = None, filled_in = True,  answer_texts = answer_texts)
    
    if request.method == "POST":
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            instance = commentform.save(commit = False)
            instance.form_id = form_id
            instance.submission_id = submission_id
            instance.save()
            return redirect(f'/dynamic-form/{form_id}/{submission_id}/?page={page_obj.paginator.num_pages}#comment-section-down')
    else:
        commentform = CommentForm()

    context = {'form_obj':form_obj, 'submission':submission, 'submission_form':submission_form, 'answer_form':answer_form, 'commentform':commentform, 'comments':comments,
               'comment_obj':page_obj}

    return render(request, 'application_and_reports_detail/dynamic_form_detail.html', context = context)

def submissions_table(request):

    # MAKE SURE YOU FILTER OUT THE RECIPIENT AGREEMENTS!

    sublist = Submission.objects.all()

    if request.user.is_staff == False and request.user.is_superuser == False:
        sublist = Submission.objects.filter(submitted_by = request.user.username)

    query = request.GET.get('search')
    if query:
        sublist = sublist.filter(
            Q(submitted_by__icontains=query) |
            Q(form__name__icontains=query) |
            Q(school_district__name__icontains=query) |
            Q(submitted_at__icontains=query)
        )
    
    date_query_before = request.GET.get('search_date_before')
    if date_query_before:
        sublist = sublist.filter(submitted_at__lte=date_query_before)
    
    date_query_after = request.GET.get('search_date_after')
    if date_query_after:
        sublist = sublist.filter(submitted_at__gte=date_query_after)

    paginator = Paginator(sublist, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'sublist':sublist, 'page_obj':page_obj, 'query':query, 'date_query_before':date_query_before, 'date_query_after':date_query_after}

    return render(request, 'application_listing_pages/submissions_table.html', context = context)

def create_pdf(request, form_id, submission_id):

    form_obj = get_object_or_404(Form, id = form_id)

    # Read in the Submission object.
    
    submission = get_object_or_404(Submission, id = submission_id)
    submission_form = SubmissionForm(instance = submission)

    district_id = submission_form['school_district'].value()
    district_name = SchoolDistrict.objects.get(pk=district_id)

    # Read in the Answer objects.

    questions = Question.objects.filter(form = form_obj)
    answers = Answer.objects.filter(submission_id = submission_id)

    answer_texts = []
    for i in answers:
        answer_texts.append(i.answer_text)

    print(answer_texts)

    answer_form = build_answer_form(questions, data = None, filled_in = True,  answer_texts = answer_texts)

    context = {'form_obj':form_obj, 
               'submission':submission, 
               'submission_form':submission_form, 
               'answer_form':answer_form, 
               'answer_texts':answer_texts,
               'district_name':district_name}

    template_path = 'application_and_reports_detail/dynamic_form_detail_pdf.html'
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest = response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


















def recipient_form(request, reference_submission):

    form_obj = get_object_or_404(Form, id=2)
    questions = Question.objects.filter(form=form_obj)
    reference_submission = get_object_or_404(Submission, id = reference_submission)

    today = datetime.today()
    reference_first = reference_submission.first_name
    reference_last = reference_submission.last_name
    reference_project_title = reference_submission.project_name
    reference_email = reference_submission.email
    reference_school_district = reference_submission.school_district
    answer_texts = [today, reference_first + ' ' + reference_last, reference_project_title, reference_email, reference_school_district, '', '']

    data = {'first_name':reference_first,
                'last_name':reference_last,
                'email':reference_email,
                'project_name':reference_project_title,
                'school_district':reference_school_district
                }    
    
    submission_form = SubmissionForm(initial=data)

    if request.method == 'POST':

        submission_form = SubmissionForm(request.POST)
        answer_form = build_answer_form(questions, request.POST)
        
        if submission_form.is_valid() and answer_form.is_valid():

            submission = submission_form.save(commit=False)
            submission.submitted_by = request.user.username
            submission.form = form_obj
            submission.save()

            for question in questions:
                Answer.objects.create(
                    submission=submission,
                    question=question,
                    answer_text=answer_form.cleaned_data.get(f'question_{question.id}', '')
                )
                
            return redirect('app:home')
    else:
        submission_form = SubmissionForm(initial = data)
        answer_form = build_answer_form(questions, data = None, filled_in = True, answer_texts = answer_texts)

    return render(request, 'application_and_reports/recipient_agreement_new.html', {
        'form_obj': form_obj,
        'submission_form': submission_form,
        'answer_form': answer_form,
    })

