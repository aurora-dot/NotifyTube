from django import forms

from notifier.models import Subscription, YouTubeQuery


class YouTubeQueryForm(forms.ModelForm):
    class Meta:
        model = YouTubeQuery
        fields = ["query"]
        widgets = {
            "query": forms.TextInput(
                attrs={
                    "class": "w-1/2 border-0 rounded-full p-2 pl-3 pl-r ring-1 ring-inset ring-gray-500 focus:ring-purple-500 hover:ring-purple-500 placeholder:text-gray-400 focus:ring-2 focus:ring-inset",
                    "required": "true",
                    "placeholder": "Search...",
                }
            ),
        }


class YouTubeEmailSubscription(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full border-0 rounded-full p-2 pl-3 pl-r ring-1 ring-inset ring-gray-500 focus:ring-purple-500 hover:ring-purple-500 placeholder:text-gray-400 focus:ring-2 focus:ring-inset"
            }
        ),
    )

    class Meta:
        model = Subscription
        fields = ["email_frequency"]
        labels = {"email_frequency": "Frequency"}
        widgets = {
            "email_frequency": forms.Select(attrs={"class": "", "required": True})
        }
