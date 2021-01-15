from django import forms
from .models import Email

class EmailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "valaki@valami.com"}))
    class Meta:
        model = Email
        fields = [
            "email"
        ]