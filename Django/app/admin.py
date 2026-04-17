from django.contrib import admin
from .models import SchoolDistrict, Form, Question, Submission, Answer

# admin.site.register(SchoolDistrict)
# admin.site.register(Form)
admin.site.register(Question)

from django.contrib import admin
from .models import SchoolDistrict, Form, Question, Submission, Answer

# Register your models here.

# This is how we can sort the submissions and let admin filter by school district or form
# Could be improved still - but it is easier to read
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ['question', 'answer_text']
    can_delete = False

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['form', 'school_district', 'last_name', 'first_name', 'submitted_at']
    list_filter = ['form', 'school_district', 'submitted_at']
    search_fields = ['first_name', 'last_name', 'email', 'project_name']
    readonly_fields = ['form', 'school_district', 'first_name', 'last_name', 
                       'email', 'project_name', 'submitted_at']
    inlines = [AnswerInline]

@admin.register(SchoolDistrict)
class SchoolDistrictAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# making questions show inline when editing
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['order', 'question_text', 'field_type', 'required']
    ordering = ['form','order']

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ['name', 'due_date']
    fields = ['name', 'due_date', 'intro_text', 'footer_text', 'footer_link', 'footer_link_label']
    inlines = [QuestionInline]

# def generatepdf(data: dict, output_path: str):
#     pdf = FPDF()