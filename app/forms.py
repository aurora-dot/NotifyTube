from django import forms

from notifier.models import YouTubeQuery


class YouTubeQueryForm(forms.ModelForm):
    class Meta:
        model = YouTubeQuery
        fields = ["query"]
        widgets = {
            "query": forms.TextInput(
                attrs={
                    "class": "",
                    "required": "true",
                }
            ),
        }
