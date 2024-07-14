"""
Views for app django application
"""

from django.shortcuts import redirect
from django.views.generic import FormView, ListView

from app.forms import YouTubeQueryForm
from notifier.lib.database_iterator import add_new_search_query
from notifier.models import YouTubeQuery, YouTubeVideo


# Create your views here.
class IndexView(FormView):
    template_name = "app/index.html"
    form_class = YouTubeQueryForm

    def post(self, request, *args, **kwargs):
        if "query" in request.POST:
            search_query = request.POST["query"]
            if not YouTubeQuery.objects.filter(query=search_query).exists():
                # this should be on a seperate thread and redirect to a loading page
                # which waits for it to finish getting first video
                add_new_search_query(search_query)
            return redirect("app:query", slug=search_query)
        else:
            raise KeyError("No `search_query` key in post request")


class QueryView(ListView):
    template_name = "app/query.html"
    model = YouTubeVideo

    def get_queryset(self):
        qs = (
            self.model.objects.filter(
                youtube_query__query=self.kwargs.get("slug"),
            )
            .prefetch_related("youtube_channel")
            .prefetch_related("youtube_query")
            .order_by("-created_at")
        )
        return qs
