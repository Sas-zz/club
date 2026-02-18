from django.urls import path
from .views import scoreboard_view

urlpatterns = [
    path("", scoreboard_view),
]
