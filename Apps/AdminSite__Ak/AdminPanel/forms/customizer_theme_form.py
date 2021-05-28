from django import forms
from Apps.AdminSite__Ak.AdminPanel.models import Customize_Theme


class customizer_theme_form(forms.ModelForm):
    class Meta:
        model = Customize_Theme
        fields='__all__'
        widgets = {
            'menu_color': forms.Select(attrs={
                'class': 'd-none'
            }),
            'theme_color': forms.Select(attrs={
                'class': 'd-none'
            }),
            'menu_mode': forms.CheckboxInput(attrs={
                'class': 'd-none'
            }),
            'header_color': forms.Select(attrs={
                'class': 'd-none'
            }),
            'header_mode': forms.Select(attrs={
                'class': 'd-none'
            }),
            'footer_mode': forms.Select(attrs={
                'class': 'd-none'
            }),
            'flash_navigation_mode': forms.CheckboxInput(attrs={
                'class': 'd-none'
            }),
        }
