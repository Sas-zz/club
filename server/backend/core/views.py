import json
import random
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, SessionCode
from .game_state import USER_PROGRESS


# ------------------------
# Round Data
# ------------------------

ROUND1 = [
    {"id": 1, "location": "Location 1", "code": "1111111111"},
    {"id": 2, "location": "Location 2", "code": "2222222222"},
    {"id": 3, "location": "Location 3", "code": "3333333333"},
]


# ------------------------
# Helpers
# ------------------------

def generate_10_digit():
    return str(random.randint(1000000000, 9999999999))


def get_user_from_session(session_code):
    try:
        session = SessionCode.objects.get(code=session_code)
        return session.user
    except SessionCode.DoesNotExist:
        return None


# ------------------------
# Login
# ------------------------

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        if not password.isdigit() or len(password) != 10:
            return JsonResponse({"error": "Password must be 10 digits"}, status=400)

        try:
            user = User.objects.get(username=username, password=password)

            # single device login
            SessionCode.objects.filter(user=user).delete()
            session = SessionCode.objects.create(user=user)

            # reset password
            user.password = generate_10_digit()
            user.save()

            # initialize progress
            USER_PROGRESS[str(session.code)] = {
                "current_set": 1,
                "rounds_completed": 0,
                "last_completed_time": None
            }

            return JsonResponse({
                "session_code": str(session.code)
            })

        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=401)


# ------------------------
# Verify Round 1
# ------------------------

@csrf_exempt
def verify_round1(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_code = data.get("session_code")
        entered_code = data.get("code")

        if not entered_code.isdigit() or len(entered_code) != 10:
            return JsonResponse({"error": "Code must be 10 digits"}, status=400)

        user = get_user_from_session(session_code)
        if not user:
            return JsonResponse({"error": "Invalid session"}, status=401)

        if session_code not in USER_PROGRESS:
            USER_PROGRESS[session_code] = {
                "current_set": 1,
                "rounds_completed": 0,
                "last_completed_time": None
            }

        current_set = USER_PROGRESS[session_code]["current_set"]
        correct_code = ROUND1[current_set - 1]["code"]

        if entered_code == correct_code:

            if current_set == 3:
                # round completed
                USER_PROGRESS[session_code]["rounds_completed"] += 1
                USER_PROGRESS[session_code]["last_completed_time"] = datetime.now()
                USER_PROGRESS[session_code]["current_set"] = 1

                return JsonResponse({
                    "completed": True,
                    "word": "hello"
                })

            USER_PROGRESS[session_code]["current_set"] += 1

            return JsonResponse({
                "success": True,
                "next_set": current_set + 1
            })

        return JsonResponse({"success": False})



import random
from datetime import datetime


# ------------------------
# Start Round 2
# ------------------------

@csrf_exempt
def start_round2(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_code = data.get("session_code")

        user = get_user_from_session(session_code)
        if not user:
            return JsonResponse({"error": "Invalid session"}, status=401)

        if session_code not in USER_PROGRESS:
            return JsonResponse({"error": "User not initialized"}, status=400)

        # generate 5 digit number
        number = random.randint(10000, 99999)

        USER_PROGRESS[session_code]["round2_number"] = number

        return JsonResponse({
            "number": number
        })


# ------------------------
# Verify Round 2
# ------------------------

@csrf_exempt
def verify_round2(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_code = data.get("session_code")
        answer = data.get("answer")

        user = get_user_from_session(session_code)
        if not user:
            return JsonResponse({"error": "Invalid session"}, status=401)

        if session_code not in USER_PROGRESS:
            return JsonResponse({"error": "User not initialized"}, status=400)

        original = USER_PROGRESS[session_code].get("round2_number")

        if not original:
            return JsonResponse({"error": "Round2 not started"}, status=400)

        correct_answer = original * 2

        if int(answer) == correct_answer:

            USER_PROGRESS[session_code]["rounds_completed"] += 1
            USER_PROGRESS[session_code]["last_completed_time"] = datetime.now()

            return JsonResponse({
                "completed": True
            })

        return JsonResponse({
            "success": False
        })

@csrf_exempt
def get_progress(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_code = data.get("session_code")

        user = get_user_from_session(session_code)
        if not user:
            return JsonResponse({"error": "Invalid session"}, status=401)

        progress = USER_PROGRESS.get(session_code, {
            "rounds_completed": 0
        })

        return JsonResponse({
            "rounds_completed": progress["rounds_completed"]
        })

# ------------------------
# ROUND 3 CONFIG
# ------------------------

ROUND3_WORD = "aAbRcEde"


# ------------------------
# Start Round 3
# ------------------------

@csrf_exempt
def start_round3(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_code = data.get("session_code")

        user = get_user_from_session(session_code)
        if not user:
            return JsonResponse({"error": "Invalid session"}, status=401)

        if session_code not in USER_PROGRESS:
            return JsonResponse({"error": "User not initialized"}, status=400)

        # initialize index
        USER_PROGRESS[session_code]["round3_index"] = 0

        first_char = ROUND3_WORD[0]

        return JsonResponse({
            "ascii": ord(first_char)
        })


# ------------------------
# Verify Round 3
# ------------------------

@csrf_exempt
def verify_round3(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_code = data.get("session_code")
        answer = data.get("answer")

        user = get_user_from_session(session_code)
        if not user:
            return JsonResponse({"error": "Invalid session"}, status=401)

        if session_code not in USER_PROGRESS:
            return JsonResponse({"error": "User not initialized"}, status=400)

        index = USER_PROGRESS[session_code].get("round3_index", 0)

        # -------------------------
        # ASCII → CHARACTER PHASE
        # -------------------------
        if index < len(ROUND3_WORD):

            correct_char = ROUND3_WORD[index]

            # user must type correct character
            if answer == correct_char:

                index += 1
                USER_PROGRESS[session_code]["round3_index"] = index

                # finished all characters
                if index == len(ROUND3_WORD):
                    return JsonResponse({
                        "final_phase": True,
                        "message": "Enter only CAPITAL letters"
                    })

                next_char = ROUND3_WORD[index]

                return JsonResponse({
                    "success": True,
                    "next_ascii": ord(next_char)
                })

            return JsonResponse({"success": False})

        # -------------------------
        # FINAL WORD PHASE
        # -------------------------
        else:
            capital_letters = "".join(
                [c for c in ROUND3_WORD if c.isupper()]
            )

            if answer == capital_letters:

                USER_PROGRESS[session_code]["rounds_completed"] += 1
                USER_PROGRESS[session_code]["last_completed_time"] = datetime.now()

                return JsonResponse({
                    "completed": True
                })

            return JsonResponse({
                "success": False,
                "message": "Wrong final word"
            })


@csrf_exempt
def verify_round4(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_code = data.get("session_code")
        answer = data.get("answer")

        user = get_user_from_session(session_code)
        if not user:
            return JsonResponse({"error": "Invalid session"}, status=401)

        if session_code not in USER_PROGRESS:
            return JsonResponse({"error": "User not initialized"}, status=400)

        # must complete previous 3 rounds
        if USER_PROGRESS[session_code]["rounds_completed"] < 3:
            return JsonResponse({"error": "Complete previous rounds"}, status=403)

        if answer == "heyyyy":

            USER_PROGRESS[session_code]["rounds_completed"] += 1
            USER_PROGRESS[session_code]["last_completed_time"] = datetime.now()

            return JsonResponse({
                "completed": True,
                "word": "you"
            })

        return JsonResponse({
            "success": False
        })
