from django import forms

class DataForm(forms.Form):
    name=forms.CharField(label="Name",max_length=100)