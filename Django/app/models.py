from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
#  Making an abstract base model since all 3 forms will use these specific fields

class BaseSubmission(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    school_district = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

def validate_file_size(value):
    constant = 5
    limit = constant * 1024 * 1024
    if value.size > limit:
        raise ValidationError(f'File too large. Size should not exceed {constant} MB.')

class Document(models.Model):
    description = models.CharField(max_length = 48, blank = True)
    document = models.FileField(upload_to='documents/', validators = [validate_file_size])
    document_name = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add = True)
    uploaded_by = models.TextField()

class SchoolDistrict(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# Testing - creating a dynamic form class
class Form(models.Model):
    name = models.CharField(max_length=200)
    due_date = models.DateField()
    intro_text = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)
    footer_link = models.URLField(blank=True)
    footer_link_label = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    FIELD_TYPES = [
        ('text', 'Short Text'),
        ('textarea', 'Long Text'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('url', 'URL'),
        ('tel', 'Phone Number'),
        ('decimal', 'Decimal Number'),
    ]
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.form.name} - {self.question_text[:50]}"


class Submission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.PROTECT)
    school_district = models.ForeignKey(SchoolDistrict, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    project_name = models.CharField(max_length=200)
    submitted_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.TextField()

    def __str__(self):
        return f"{self.form.name} - {self.school_district} - {self.submitted_at}"
    
class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer_text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.question.question_text[:30]} - {self.answer_text[:30]}"

class Comment(models.Model):

    name = models.CharField(max_length = 100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    form = models.ForeignKey(Form, on_delete = models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete = models.CASCADE)