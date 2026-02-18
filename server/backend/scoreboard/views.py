from django.shortcuts import render
from core.game_state import USER_PROGRESS
from core.models import SessionCode


def scoreboard_view(request):
    players = []

    for session_code, data in USER_PROGRESS.items():
        try:
            session = SessionCode.objects.get(code=session_code)

            players.append({
                "username": session.user.username,
                "rounds": data["rounds_completed"],
                "time": data["last_completed_time"]
            })

        except:
            continue 

    # Sorting Logic
    # 1️⃣ Higher rounds first
    # 2️⃣ Earlier completion time first

    players.sort(
        key=lambda x: (
            -x["rounds"],
            x["time"] if x["time"] else float("inf")
        )
    )

    return render(request, "scoreboard.html", {"players": players})
