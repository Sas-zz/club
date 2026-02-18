from django.urls import path
from .views import login, verify_round1

from .views import (
    login,
    verify_round1,
    start_round2,
    verify_round2,
    get_progress,
    start_round3,
    verify_round3,
    verify_round4,
)

urlpatterns = [
    path("login/", login),
    path("verify-round1/", verify_round1),

    path("start-round2/", start_round2),
    path("verify-round2/", verify_round2),
    path("progress/", get_progress),
    path("start-round3/", start_round3),
    path("verify-round3/", verify_round3),
    path("verify-round4/", verify_round4),



]
