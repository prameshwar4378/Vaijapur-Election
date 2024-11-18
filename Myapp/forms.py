
from django import forms
from .models import Vote, Candidate

class VoteForm(forms.ModelForm):
    candidate = forms.ModelChoiceField(
        queryset=Candidate.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,  # Remove the "-------" default choice
        label="Choose a Candidate"
    )

    class Meta:
        model = Vote
        fields = ['candidate']