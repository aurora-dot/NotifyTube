from django import forms

from notifier.models import Subscription, YouTubeQuery


class YouTubeQueryForm(forms.ModelForm):
    class Meta:
        model = YouTubeQuery
        fields = ["query"]
        widgets = {
            "query": forms.TextInput(
                attrs={
                    "class": "sm:w-1/2 w-full border-0 rounded-full p-2 pl-3 pl-r ring-1 ring-inset ring-gray-500 focus:ring-purple-500 hover:ring-purple-500 placeholder:text-gray-400 focus:ring-2 focus:ring-inset",
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
                "class": "text-sm w-full border-0 rounded-full p-2 pl-3 pl-r ring-1 ring-inset ring-gray-300 focus:ring-purple-500 hover:ring-purple-500 placeholder:text-gray-400 focus:ring-2 focus:ring-inset"
            }
        ),
    )

    class Meta:
        model = Subscription
        fields = ["email_frequency"]
        labels = {"email_frequency": "Frequency"}
        widgets = {
            "email_frequency": forms.Select(
                attrs={
                    "class": "block w-full pl-3 pr-10 py-1.5 text-sm border-0 ring-gray-300 focus:outline-none hover:ring-purple-500 focus:ring-purple-500 ring-1 focus:ring-2 focus:ring-inset rounded-md",
                    "required": True,
                }
            )
        }
