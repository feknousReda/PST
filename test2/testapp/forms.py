from django import forms

MODULES_CHOICES = (

('book1','book1'),
('book2','book2'),
('book3','book3'),

)

class SimpleForm(forms.Form):
    favorite_modules = forms.MultipleChoiceField(
        widget = forms.CheckBoxSelectMultiple,
        choices = MODULES_CHOICES,
    )
