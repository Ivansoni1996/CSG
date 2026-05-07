from django import forms
from .models import Members

class MemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['member_id', 'email', 'name', 'family_name', 'status', 'amount']
