import json

from django.http import HttpResponse, JsonResponse
from rest_framework import generics

from notifier.lib.database_iterator import add_new_search_query
from notifier.models import YouTubeQuery

# def post(self, request, *args, **kwargs):
#     if "query" in request.POST:
#         search_query = request.POST["query"]
#         if not YouTubeQuery.objects.filter(query=search_query).exists():
#             # this should be on a separate thread and redirect to a loading page
#             # which waits for it to finish getting first video
#             add_new_search_query(search_query)
#         return redirect("app:query", slug=search_query)
#     else:
#         return HttpResponse(status_code=400)


# Create your views here.
class Search(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        request_json = json.loads(request.body.decode("utf-8"))
        if "query" in request_json:
            search_query = request_json["query"]
            if not YouTubeQuery.objects.filter(query=search_query).exists():
                add_new_search_query(search_query)
            return JsonResponse(
                {
                    "message": "successful",
                    "redirect": f"/search/{search_query}/",
                }
            )

        else:
            return HttpResponse(status=400)
