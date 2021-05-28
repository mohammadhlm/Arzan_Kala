from django import forms


class Activation_link_submission_form(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())


class Change_User_Information(forms.Form):
    gender_selection_choices = [
        ('MS', 'زن'),
        ('MR', 'مرد'),
        ('TG', 'دیگر'),
    ]

    first_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    last_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    user_profile = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "d-none"
    }))
    gender_selection = forms.ChoiceField(required=False, choices=gender_selection_choices, widget=forms.Select(attrs={
        "class": "form-control"
    }))
    postal_code = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    phone_number = forms.CharField(required=False, max_length=11, widget=forms.NumberInput(attrs={
        "class": "form-control"
    }))
    location_first = forms.CharField(required=False, max_length=250, widget=forms.Textarea(attrs={
        "class": "form-control"
    }))
