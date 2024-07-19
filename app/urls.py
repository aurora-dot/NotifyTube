"""
Paths for app django application
"""

from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/<slug>/", views.QueryView.as_view(), name="query"),
    path(
        "unsubscribe/success/",
        views.UnsubscribeSuccessView.as_view(),
        name="unsubscribe_success",
    ),
    path("unsubscribe/<slug>/", views.UnsubscribeView.as_view(), name="unsubscribe"),
]
