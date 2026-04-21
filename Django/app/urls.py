from django.urls import include, path
from . import views

app_name = 'app'

urlpatterns = [

    path('', views.home, name='home'),
    path('directory', views.directory, name = 'directory'),
    path('recipient_agreement/', views.recipient_agreement, name='recipient_agreement'),
    path('w9_upload/', views.w9_upload, name='w9_upload'),

    # Kinley Blank Forms to Submit

    path("recipient-agreement/", views.recipient_agreement, name="recipient_agreement"),

    # Link to the blank dynamic form, with a parameter designating which one (hope grant, mid-year, end-year)

    path("dynamic-form/<int:form_id>", views.dynamic_form, name="dynamic_form"),

    # Link to a filled dynamic form, with parameters designating the form type, and then the submission number

    path("dynamic-form/<int:form_id>/<int:submission_id>/", views.dynamic_form_detail, name="dynamic_form_detail"),

    # Link to a filled recipient agreement, with parameters designating the form type, and then the submission number

    path("recipient-agreement/<int:form_id>/<int:submission_id>/", views.recipient_agreement_detail, name="recipient_agreement_detail"),

    # Link to an initial recipient agreement, with a parameter referencing the original submission it is in response to.

    path("recipient-form-create/<int:reference_submission>/", views.recipient_form, name="recipient_form"),

    # Link to create a PDF from a subnmitted form.

    path("dynamic-pdf/<int:form_id>/<int:submission_id>/", views.create_pdf, name="create_pdf"),

    # Link to a page containing a table of submitted applications.

    path("submissions_table", views.submissions_table, name="submissions_table"),

    # Link to recipient agreements.

    path("agreements_table", views.agreements_table, name="agreements_table"),

    # Uploaded Files

    path("documents_table", views.documents_table, name="documents_table"),

    # Download a Document

    path("document-download/<int:id>/", views.download_view, name="download_view"),

]