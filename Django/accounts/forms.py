from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm as DjangoSetPasswordForm
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    #prevent user from registering with duplicate email
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    
    #allow user to change password
    class SetPasswordForm(DjangoSetPasswordForm):

        def __init__(self, user, *args, **kwargs):
            super().__init__(user, *args, **kwargs)
            
class ForgotUsernameForm(forms.Form):
    email = forms.EmailField()