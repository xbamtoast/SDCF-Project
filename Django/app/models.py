from django.db import models

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

# Inherits properties from base submission class
class HopeGrantApplication(BaseSubmission):
    # Program Title
    program_title = models.CharField(max_length=200)

    # Fields for superintendent info
    superintendent_first_name = models.CharField(max_length=100)
    superintendent_last_name = models.CharField(max_length=100)
    superintendent_phone = models.CharField(max_length=20)
    superintendent_email = models.EmailField()

    # Primary contact info fields
    primary_contact_first_name = models.CharField(max_length=100)
    primary_contact_last_name = models.CharField(max_length=100)
    primary_contact_phone = models.CharField(max_length=20)
    primary_contact_email = models.EmailField()

    # Address fields
    address_street = models.CharField(max_length=200)
    address_city = models.CharField(max_length=100)
    address_state = models.CharField(max_length=2)
    address_zip = models.CharField(max_length=10)

    # Amount resquested field
    grant_amount_requested = models.DecimalField(max_digits=10, decimal_places=2)

    # Text input questions
    project_summary = models.TextField()
    needs_statement = models.TextField()
    impact_children = models.TextField()
    impact_other_individuals = models.TextField()
    impact_long_term = models.TextField()
    collaboration = models.TextField()
    budget = models.TextField()
    success = models.TextField()

class MidYearReport(BaseSubmission):
    # Main text input questions
    progress_update = models.TextField()
    unexpected_difficulties = models.TextField()
    successes = models.TextField()
    additional_comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project_name} - Mid-Year Report"
    
    
class EndYearReport(BaseSubmission):
    title = models.CharField(max_length=100)

    # Report questions
    project_overview = models.TextField()
    children_impacted = models.TextField()
    other_individuals_impacted = models.TextField()
    long_term_impact = models.TextField()
    hope_impact = models.TextField()
    remaining_funds = models.TextField()
    budget = models.TextField()
    what_worked_well = models.TextField()
    challenges = models.TextField()
    story_1 = models.TextField()
    story_2 = models.TextField(blank=True)
    future_funding = models.TextField()
    video_link = models.URLField()

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.project_name}"