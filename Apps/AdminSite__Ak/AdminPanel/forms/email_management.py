from django import forms
from Apps.AdminSite__Ak.AdminPanel.models import Email_Management


class Email_Management_Form(forms.ModelForm):
    class Meta:
        model = Email_Management
        exclude = (
            'send_date',
            'number_of_submissions'
        )
        widgets = {
            'user': forms.SelectMultiple(attrs={
                "class": "select2 form-control"
            }),
            'subject': forms.TextInput(attrs={
                "class": "form-control"
            }),
        }


class remove_mail_form(forms.Form):
    removed_mail_id = forms.CharField()
