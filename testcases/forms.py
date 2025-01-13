from django import forms

class TestCaseForm(forms.Form):
    test_case_data = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 50}))
