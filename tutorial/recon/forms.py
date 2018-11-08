from django import forms

class HomeForm(forms.Form):
    Domaine = forms.CharField()

MODULES_CHOICES = (

    ('google_site_web','google_site_web'),
    ('bing_domain_web','bing_domain_web'),
    ('netcraft','netcraft'),
    ('hackertarget','hackertarget'),
    ('brute_hosts','brute_hosts'),

)

class SimpleForm(forms.Form):
    favorite_modules = forms.MultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
        choices = MODULES_CHOICES,
    )
