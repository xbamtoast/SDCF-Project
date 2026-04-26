from django.contrib import admin
from .models import SchoolDistrict, Form, Question, Submission, Answer

from django.contrib import admin
from .models import SchoolDistrict, Form, Question, Submission, Answer, Comment

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
    fields = ['name', 'due_date', 'intro_text', 'footer_text', 'footer_link', 'footer_link_label', 'is_active']
    inlines = [QuestionInline]

# Function for cloning a form
    actions = ["clone_form"]
    def clone_form(self, request, queryset):
        for form in queryset:
            old_form_id = form.id

            form.pk = None
            form.name = f"{form.name} (Copy)"
            form.save()
            new_form = form

            questions = Question.objects.filter(form_id=old_form_id).order_by("order")
            print('Found:', questions.count())

            for q in questions:
                q.pk = None
                q.form = new_form
                q.save()

    clone_form.short_description = "Duplicate Form"

admin.site.register(Comment)
admin.site.register(Question)