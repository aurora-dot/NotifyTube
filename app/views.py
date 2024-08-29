"""
Views for app django application
"""

from typing import Any

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import DeleteView

from app.forms import YouTubeEmailSubscription, YouTubeQueryForm
from notifier.models import Email, Subscription, YouTubeQuery, YouTubeVideo


# Create your views here.
class IndexView(TemplateView):
    template_name = "app/index.html"


class QueryView(ListView):
    template_name = "app/query.html"
    model = YouTubeVideo

    def post(self, request, *args, **kwargs):
        if "email_frequency" in request.POST and "email" in request.POST:
            email = request.POST["email"]
            frequency = request.POST["email_frequency"]

            email_obj, _ = Email.objects.get_or_create(email=email)
            query = YouTubeQuery.objects.filter(
                query=self.kwargs.get("slug"),
            ).get()
            Subscription.objects.update_or_create(
                email=email_obj, query=query, defaults={"email_frequency": frequency}
            )

            self.object_list = self.get_queryset()  # pylint: disable=W0201
            return render(
                request,
                self.template_name,
                self.get_context_data() | {"success": True},
            )
        else:
            return HttpResponse(status=400)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = YouTubeQueryForm()
        context["email_form"] = YouTubeEmailSubscription()
        return context

    def get_queryset(self):
        return (
            self.model.objects.filter(
                youtube_query__query=self.kwargs.get("slug"),
            )
            .prefetch_related("youtube_channel")
            .prefetch_related("youtube_query")
            .order_by("-created_at")
        )


class UnsubscribeView(DeleteView):
    model = Subscription
    template_name = "app/unsubscribe.html"
    success_url = reverse_lazy("app:unsubscribe_success")


class UnsubscribeSuccessView(TemplateView):
    template_name = "app/unsubscribe_success.html"
