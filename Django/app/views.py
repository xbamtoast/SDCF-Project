# Django Imports

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template

# Django Project Imports

from .forms import DocumentFormTest
from .forms import SubmissionForm, CommentForm, build_answer_form
from .models import Form, Question, Submission, Document, Answer, SchoolDistrict, Comment, UserSignature

# Other Imports

import base64
from datetime import datetime
import json
from pathlib import Path
from xhtml2pdf import pisa
import uuid

# Import variable

recipient_agreement = Form.objects.filter(name__icontains='agree').first()
recipient_agreement_id = recipient_agreement.id if recipient_agreement else -1

# Home/landing page view

def directory(request):
    return render(request, 'miscellaneous/directory.html')

def home(request):
    forms = Form.objects.filter(is_active = True)
    return render(request, "landing.html", {"forms": forms})

def landing_page(request):
    return render(request, 'landing.html')

# This view helps upload documents (namely, W9s) to the media folder.

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentFormTest(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.uploaded_by = request.user
            instance.document_name = str(instance.document).replace('documents/', '')
            instance.save()
            return redirect('app:home')
        else:
            print(form.errors)
    else:
        form = DocumentFormTest()

    return render(request, 'miscellaneous/w9_upload.html', {'form': form})

# This view helps download documents from the media folder on the documents table page.

@login_required
def download_document(request, id):

    # Get the document object from the database.

    document_object = get_object_or_404(Document, id = id)

    # Check if the current user is staff. 
    # If they are not staff, check if the current user uploaded the document object.
    # If this check fails, send them to the Permission Denied page.

    if request.user.is_staff == False:
        if document_object.uploaded_by != request.user.username:
            return render(request, 'miscellaneous/permission_denied.html')
    
    # Point to the media folder.

    document_path = 'media/' + str(document_object.document)
    print(document_path)
    # Store the filename for the download.
    
    filename = Path(document_path)
    filename = filename.name
    
    # Is it a text file or a PDF?

    if document_path[-3:] in ('txt', 'csv'):
        response = FileResponse(open(document_path, 'rb'), as_attachment = True, filename = filename, content_type = 'text/plain')
    else:
        response = FileResponse(open(document_path, 'rb'), as_attachment = True, filename = filename, content_type = 'application/pdf')

    return response

# Blank Recipient Agreement View

def recipient_agreement(request): #view to render recipient agreement
    return render(request, 'application_and_reports/recipient_agreement.html')

# View for a blank dynamic form.

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

# View for a dynamic form with filled in data from a submission.

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

# Award Agreement View

def recipient_form(request, reference_submission):

    if recipient_agreement_id == -1:
        forms = Form.objects.filter(is_active = True)
        return render(request, "landing.html", {"forms": forms})
    else:
        form_obj = get_object_or_404(Form, id = recipient_agreement_id)

    questions = Question.objects.filter(form=form_obj)
    reference_submission = get_object_or_404(Submission, id = reference_submission)

    today = datetime.today()
    reference_first = reference_submission.first_name
    reference_last = reference_submission.last_name
    reference_project_title = reference_submission.project_name
    reference_email = reference_submission.email
    reference_school_district = reference_submission.school_district
    reference_user = reference_submission.submitted_by

    answer_texts = [today, reference_first + ' ' + reference_last, reference_email, '', '', '', '']

    data = {'first_name':reference_first,
                'last_name':reference_last,
                'email':reference_email,
                'project_name':reference_project_title,
                'school_district':reference_school_district,
                'submitted_by':reference_user
                }    
    
    submission_form = SubmissionForm(initial=data)

    if request.method == 'POST':

        submission_form = SubmissionForm(request.POST)
        answer_form = build_answer_form(questions, request.POST)
        
        if submission_form.is_valid() and answer_form.is_valid():

            submission = submission_form.save(commit=False)
            submission.submitted_by = reference_user
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

# View for a recipient agreement with filled in data from a submission.

def recipient_agreement_detail(request, form_id, submission_id):

    # Read in the Form object.

    form_obj = get_object_or_404(Form, id = form_id)

    # Fetch the signature if it already exists. Otherwise, it is empty and the user will be able to sign it.

    signature_obj = UserSignature.objects.filter(submission = submission_id)
    if signature_obj:
        signature_obj = signature_obj[0]

    # Read in the Submission object.
    
    submission = get_object_or_404(Submission, id = submission_id)
    submission_form = SubmissionForm(instance = submission)
    target_user = submission.submitted_by

    # Check if the user is staff, or if the user is tied to this award agreement.

    if ((request.user.is_staff == False) and (request.user.is_superuser == False)):
        if (submission.submitted_by != request.user.username): 
            return render(request, 'miscellaneous/permission_denied.html', context = {})

    # Read in the Answer objects.

    questions = Question.objects.filter(form = form_obj)
    answers = Answer.objects.filter(submission_id = submission_id)

    answer_texts = []
    for i in answers:
        answer_texts.append(i.answer_text)   

    answer_form = build_answer_form(questions, data = None, filled_in = True,  answer_texts = answer_texts)

    if "award_data_save" in request.POST:

        submission_form = SubmissionForm(request.POST, instance = submission)
        answer_form = build_answer_form(questions, request.POST)

        if submission_form.is_valid() and answer_form.is_valid():

            submission = submission_form.save(commit=False)
            submission.submitted_by = target_user
            submission.form = form_obj
            submission.save()

            new_texts = []
            for question in questions:
                new_texts.append(answer_form.cleaned_data.get(f'question_{question.id}', ''))

            for i in range(0, len(answers)):
                Answer.objects.filter(id = answers[i].id).update(answer_text = new_texts[i])

    elif "signature_save" in request.POST:

        data_dict = request.POST.dict()
        json_data = json.dumps(data_dict)
        data = json.loads(json_data)
        image_data = data.get('signature')
        print(image_data)

        format, imgstr = image_data.split(';base64,') 
        ext = format.split('/')[-1] 
        
        # Decode and create a Django File object
        file_name = f"sig_{uuid.uuid4()}.{ext}"
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        
        # Save to model

        instance = UserSignature(image=data)
        instance.submission = submission_id
        instance.submitted_by = request.user.username
        instance.save()
        return redirect(request.path_info)
        
    else:

        print(submission_form.errors)
        print(answer_form.errors)
        submission_form = SubmissionForm(instance = submission)
        answer_form = build_answer_form(questions, data = None, filled_in = True,  answer_texts = answer_texts)

    context = {'form_obj':form_obj, 'submission':submission, 'submission_form':submission_form, 'answer_form':answer_form,
               'signature':signature_obj}

    return render(request, 'application_and_reports/recipient_agreement_new.html', context = context)

# View for the submissions table (no recipient agreements)

def submissions_table(request):

    # MAKE SURE YOU FILTER OUT THE RECIPIENT AGREEMENTS!

    sublist = Submission.objects.filter(
        form__name__icontains="application"
    ).exclude(
        form__name__icontains="report"
    ).exclude(
        form_id=recipient_agreement_id
    )

    # sublist = Submission.objects.exclude(form_id = recipient_agreement_id)

    if request.user.is_staff == False and request.user.is_superuser == False:
        sublist = sublist.filter(submitted_by = request.user.username)
        sublist = sublist.exclude(form_id = recipient_agreement_id)

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

    paginator = Paginator(sublist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'sublist':sublist, 'page_obj':page_obj, 'query':query, 'date_query_before':date_query_before, 'date_query_after':date_query_after}

    return render(request, 'tables/submissions_table.html', context = context)

# View for the agreements table.

def agreements_table(request):

    # MAKE SURE YOU FILTER OUT THE RECIPIENT AGREEMENTS

    sublist = Submission.objects.filter(form_id = recipient_agreement_id)

    if request.user.is_staff == False and request.user.is_superuser == False:
        sublist = Submission.objects.filter(submitted_by = request.user.username)
        sublist = sublist.filter(form_id = recipient_agreement_id)

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

    paginator = Paginator(sublist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'sublist':sublist, 'page_obj':page_obj, 'query':query, 'date_query_before':date_query_before, 'date_query_after':date_query_after}
    return render(request, 'tables/agreements_table.html', context = context)

# View to create the PDF of submissions.

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

# Documents table

def documents_table(request):

    sublist = Document.objects.all()

    if request.user.is_staff == False and request.user.is_superuser == False:
        sublist = sublist.filter(uploaded_by = request.user.username)

    query = request.GET.get('search')
    if query:
        sublist = sublist.filter(
            Q(description__icontains=query) |
            Q(document__icontains=query)
        )
    
    date_query_before = request.GET.get('search_date_before')
    if date_query_before:
        sublist = sublist.filter(uploaded_at__lte=date_query_before)
    
    date_query_after = request.GET.get('search_date_after')
    if date_query_after:
        sublist = sublist.filter(uploaded_at__gte=date_query_after)

    paginator = Paginator(sublist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'sublist':sublist, 'page_obj':page_obj, 'query':query, 'date_query_before':date_query_before, 'date_query_after':date_query_after}

    return render(request, 'tables/documents_table.html', context = context)

def reports_table(request):

    # Only show report submissions
    # Exclude recipient agreements
    sublist = Submission.objects.exclude(
        form_id=recipient_agreement_id
    ).filter(
        form__name__icontains='report'
    )

    # Restrict normal users to their own reports
    if not request.user.is_staff and not request.user.is_superuser:
        sublist = sublist.filter(
            submitted_by=request.user.username
        )

    # Search filter
    query = request.GET.get('search')
    if query:
        sublist = sublist.filter(
            Q(submitted_by__icontains=query) |
            Q(form__name__icontains=query) |
            Q(school_district__name__icontains=query) |
            Q(submitted_at__icontains=query)
        )

    # Date filters
    date_query_before = request.GET.get('search_date_before')
    if date_query_before:
        sublist = sublist.filter(
            submitted_at__lte=date_query_before
        )

    date_query_after = request.GET.get('search_date_after')
    if date_query_after:
        sublist = sublist.filter(
            submitted_at__gte=date_query_after
        )

    # Sort newest first
    sublist = sublist.order_by('-submitted_at')

    # Pagination
    paginator = Paginator(sublist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sublist': sublist,
        'page_obj': page_obj,
        'query': query,
        'date_query_before': date_query_before,
        'date_query_after': date_query_after
    }

    return render(
        request,
        'tables/reports_table.html',
        context=context
    )