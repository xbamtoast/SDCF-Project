from django import forms
from .models import MidYearReport, HopeGrantApplication, EndYearReport, ApplicationComment, MidYearComment, EndYearComment
from .models import Document

class HopeGrantApplicationForm(forms.ModelForm):
    class Meta:
        model = HopeGrantApplication
        fields = "__all__"
        widgets = {
            'project_summary': forms.Textarea(attrs={'rows': 8}),
            'needs_statement': forms.Textarea(attrs={'rows': 8}),
            'impact_children': forms.Textarea(attrs={'rows': 8}),
            'impact_other_individuals': forms.Textarea(attrs={'rows': 8}),
            'impact_long_term': forms.Textarea(attrs={'rows': 8}),
            'collaboration': forms.Textarea(attrs={'rows': 8}),
            'budget': forms.Textarea(attrs={'rows': 8}),
            'success': forms.Textarea(attrs={'rows': 8}),
        }
        labels = {
            'project_summary': '1. Please summarize your project. In approximately 150 words tell us what you plan to do, why you plan to do this project, who will be involved, and what you hope to accomplish? Is this an ongoing project or a new project?',
            'needs_statement': '2. Describe the need(s) that will be addressed through this project.',
            'impact_children': '3a. Approximately how many children and what ages/grades will be impacted during the current school year by this project?',
            'impact_other_individuals': '3b. Approximately how many other individuals will be impacted by this project this school year?',
            'impact_long_term': '3c. What is the long-term impact of this grant and how does this project bring hope to those impacted? What change will happen because of this project this school year? What long-lasting impact will this project have on students?',
            'collaboration': '4. Describe any collaborative entities the district will be working with, such as other financial support, volunteers, churches, or other resources.',
            'budget': '5. What is your project budget? How will Hope Grant funds be used? Please list major expenses expected to be funded by the grant as well as other expenses you expect to fund by the district, other grants, or funding sources.',
            'success': '6. How will you measure the success of your goal? Please share 1-3 program goals and any measurable objectives for each goal.',
        }
# Mid year report
class MidYearReportForm(forms.ModelForm):
    class Meta:
        model = MidYearReport
        fields = "__all__"
        widgets = {
            'progress_update': forms.Textarea(attrs={'rows': 6}),
            'unexpected_difficulties': forms.Textarea(attrs={'rows': 6}),
            'successes': forms.Textarea(attrs={'rows': 6}),
            'additional_comments': forms.Textarea(attrs={'rows': 6}),
        }
        labels = {
            'progress_update': '1. Please provide a quick update about the progress of your 2026-2027 Hope Grant.',
            'unexpected_difficulties': '2. Have you encountered any unexpected difficulties? If so, please explain and share how you did or plan to overcome those challenges.',
            'successes': '3. Do you have any successes or stories you can share?',
            'additional_comments': '4. Any additional information or comments you\'d like to share?',
        }


# End of year report
class EndYearReportForm(forms.ModelForm):
    class Meta:
        model = EndYearReport
        fields = '__all__'
        widgets = {
            'project_overview': forms.Textarea(attrs={'rows': 8}),
            'children_impacted': forms.Textarea(attrs={'rows': 6}),
            'other_individuals_impacted': forms.Textarea(attrs={'rows': 4}),
            'long_term_impact': forms.Textarea(attrs={'rows': 6}),
            'hope_impact': forms.Textarea(attrs={'rows': 6}),
            'remaining_funds': forms.Textarea(attrs={'rows': 4}),
            'budget': forms.Textarea(attrs={'rows': 6}),
            'what_worked_well': forms.Textarea(attrs={'rows': 6}),
            'challenges': forms.Textarea(attrs={'rows': 6}),
            'story_1': forms.Textarea(attrs={'rows': 8}),
            'story_2': forms.Textarea(attrs={'rows': 8}),
            'future_funding': forms.Textarea(attrs={'rows': 6}),
        }
        labels = {
            'title': 'Title',
            'project_overview': '1. Tell us about your 2026-2027 Hope Grant project. Did your project work out the way you envisioned? Did you accomplish the goals you wished to accomplish? What changes occurred because of this project? Did you address the needs you hoped to impact, and if so, tell us about that impact.',
            'children_impacted': '2. How many children were impacted by this project? How were these children impacted?',
            'other_individuals_impacted': '3. How many other individuals do you estimate were also impacted by this project?',
            'long_term_impact': '4. What long-term impact will this project have on your students, their families, and your community?',
            'hope_impact': '5. How did you feel this project increased hope in students? What is your definition of "hope" as it relates to this project?',
            'remaining_funds': '6. Do you have remaining funds from the Hope Grant? If so, how much?',
            'budget': '7. Budget: How were Hope Grant funds spent and how much did you spend? Please provide a general budget of how dollars were spent.',
            'what_worked_well': '8. What aspects of the project worked well, or better than expected?',
            'challenges': '9. Did you face any challenges and how were they addressed or resolved?',
            'story_1': '10. Story 1 - Please provide a written story about the impact of your grant. (Note: these stories will be shared publicly)',
            'story_2': 'Story 2',
            'future_funding': '11. If Silver Dollar City Foundation provides Hope Grant opportunities next year, do you anticipate requesting funding to continue or expand on this project, and why?',
            'video_link': '12. Video Upload Link - Please submit a video approximately 90 seconds in length that Silver Dollar City Foundation may share about how your district was impacted by your Hope Grant. Your video may include comments from administrators, counselors, teachers, or other staff. Please do not share personally identifiable information unless the family has consented. These videos may be shared publicly.',
        }

class ApplicationCommentForm(forms.ModelForm):
    class Meta:
        model = ApplicationComment
        fields = ['name', 'message']
        widgets = {
        'name': forms.Textarea(attrs={'rows': 1}),
        'message': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'name':'Name',
            'message':'Comment'
        }

class MidYearCommentForm(forms.ModelForm):
    class Meta:
        model = MidYearComment
        fields = ['name', 'message']
        widgets = {
        'name': forms.Textarea(attrs={'rows': 1}),
        'message': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'name':'Name',
            'message':'Comment'
        }

class EndYearCommentForm(forms.ModelForm):
    class Meta:
        model = EndYearComment
        fields = ['name', 'message']
        widgets = {
        'name': forms.Textarea(attrs={'rows': 1}),
        'message': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'name':'Name',
            'message':'Comment'
        }

class DocumentFormTest(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )