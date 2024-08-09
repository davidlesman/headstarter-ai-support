from django.urls import path

from .views import IndexPage, Reset, Send

urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("send/", Send.as_view(), name="send"),
    path("delete/", Reset.as_view(), name="delete"),
]
