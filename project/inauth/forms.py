# Django imports
from django import forms

# Project imports
from project.inauth.auth import Auth, ResetPassword


class AuthorizationForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(AuthorizationForm, self).clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        name = cleaned_data.get('name')

        if email and not name:
            name = email.split('@')[0]

        incheck_auth = Auth(
            email=email,
            password=password,
            **{'name': name}
        )
        if not incheck_auth.is_valid():
            raise forms.ValidationError(
                    incheck_auth.get_errors()[0])
        return cleaned_data


class PasswordResetForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        reset_request = ResetPassword(email=email)
        if not reset_request.is_valid():
            raise forms.ValidationError(
                reset_request.get_errors()[0]['email'])
        return email

