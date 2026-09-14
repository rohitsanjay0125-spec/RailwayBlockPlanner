from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "railway-block-planner-secret")


# =========================================================
# RAILRADAR CONFIG
# =========================================================

RAILRADAR_API_KEY = os.getenv("RAILRADAR_API_KEY")

RAILRADAR_URL = "https://railradar.in/api/v1/trains/live"


# =========================================================
# TRAIN LIST
# =========================================================
# These are the trains that will be requested from RailRadar.

TRAIN_NUMBERS = [
    "11078",
    "12191",
    "12780",
    "12616",
    "22692",
    "12626",
    "12628",
    "12622",
    "12533",
    "11072",
    "11058",
    "12722",
    "22537",
    "20104",
    "12854",
    "12618",
    "12138",
    "18238",
    "19343"
]


# =========================================================
# DEMO TRAIN DATA
# =========================================================

trains = [
    {
        "train_number": "11078",
        "train_name": "Jhelum Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12191",
        "train_name": "Shridham SF Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12780",
        "train_name": "Goa Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12616",
        "train_name": "Grand Trunk Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 3
    },
    {
        "train_number": "22692",
        "train_name": "Rajdhani Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 3
    },
    {
        "train_number": "12626",
        "train_name": "Kerala Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12628",
        "train_name": "Karnataka Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12622",
        "train_name": "Tamil Nadu Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12533",
        "train_name": "Pushpak Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "11072",
        "train_name": "Kamayani Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "11058",
        "train_name": "Mumbai CSMT Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12722",
        "train_name": "Dakshin SF Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "22537",
        "train_name": "Kushinagar SF Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "20104",
        "train_name": "Mumbai LTT SF Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12854",
        "train_name": "Amarkantak Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12618",
        "train_name": "Mangala Lakshadweep Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "12138",
        "train_name": "Punjab Mail",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "18238",
        "train_name": "Chhattisgarh Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 2
    },
    {
        "train_number": "19343",
        "train_name": "Penchvalley Express",
        "section": "Bhopal-Itarsi",
        "start_time": 0,
        "end_time": 24,
        "priority": 1
    }
]


# =========================================================
# ASSET DATA
# =========================================================

assets = []


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user_id = request.form.get("user_id")
        department = request.form.get("department")

        session["user_id"] = user_id
        session["department"] = department

        return redirect(url_for("index"))

    return """
    <html>
    <head>
        <title>Railway Block Planner Login</title>
    </head>

    <body style="font-family:Arial;text-align:center;margin-top:100px;">

        <h1>🚆 Railway Block Planner</h1>

        <form method="POST">

            <input
                type="text"
                name="user_id"
                placeholder="User ID"
                required
            >

            <br><br>

            <input
                type="text"
                name="department"
                placeholder="Department"
                required
            >

            <br><br>

            <button type="submit">
                Login
            </button>

        </form>

    </body>
    </html>
    """


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper


# =========================================================
# RAILRADAR - SINGLE TRAIN
# =========================================================

def get_live_train(train_number):

    if not RAILRADAR_API_KEY:
        print("ERROR: RAILRADAR_API_KEY not found in .env")
        return None

    try:

        headers = {
            "Authorization": f"Bearer {RAILRADAR_API_KEY}",
            "x-api-key": RAILRADAR_API_KEY,
            "Accept": "application/json"
        }

        params = {
            "trainNumber": train_number
        }

        response = requests.get(
            RAILRADAR_URL,
            headers=headers,
            params=params,
            timeout=15
        )

        print(
            f"RailRadar {train_number}: "
            f"HTTP {response.status_code}"
        )

        if response.status_code != 200:

            print(
                f"RailRadar {train_number}: "
                f"Request failed"
            )

            return None

        result = response.json()

        # =================================================
        # EXACT RESPONSE STRUCTURE
        #
        # {
        #   "success": true,
        #   "data": {
        #       "trainNumber": "...",
        #       "trainName": "...",
        #       "status": "...",
        #       "train": {...},
        #       "isLive": true,
        #       "trackingMode": "...",
        #       "previousHalt": {...},
        #       "nextHalt": {...},
        #       "delayMinutes": 0,
        #       "currentLocation": {...}
        #   }
        # }
        # =================================================

        if not result.get("success"):
            return None

        data = result.get("data")

        if not data:
            return None

        train_info = data.get("train", {})
        current_location = data.get(
            "currentLocation",
            {}
        )

        previous_halt = data.get(
            "previousHalt"
        )

        next_halt = data.get(
            "nextHalt"
        )

        live_train = {

            "trainNumber":
                data.get(
                    "trainNumber",
                    train_info.get(
                        "number",
                        train_number
                    )
                ),

            "trainName":
                data.get(
                    "trainName",
                    train_info.get(
                        "name",
                        "Unknown Train"
                    )
                ),

            "status":
                data.get(
                    "status",
                    "unknown"
                ),

            "isLive":
                data.get(
                    "isLive",
                    False
                ),

            "trackingMode":
                data.get(
                    "trackingMode",
                    "unknown"
                ),

            "delayMinutes":
                data.get(
                    "delayMinutes",
                    0
                ),

            "currentLocation": {

                "stationCode":
                    current_location.get(
                        "stationCode",
                        ""
                    ),

                "stationName":
                    current_location.get(
                        "stationName",
                        "Unknown"
                    ),

                "sequence":
                    current_location.get(
                        "sequence"
                    ),

                "status":
                    current_location.get(
                        "status"
                    ),

                "lat":
                    current_location.get(
                        "lat"
                    ),

                "lng":
                    current_location.get(
                        "lng"
                    )
            },

            "previousHalt": {

                "stationCode":
                    previous_halt.get(
                        "stationCode"
                    ) if previous_halt else None,

                "stationName":
                    previous_halt.get(
                        "stationName"
                    ) if previous_halt else None,

                "sequence":
                    previous_halt.get(
                        "sequence"
                    ) if previous_halt else None,

                "distance":
                    previous_halt.get(
                        "distance"
                    ) if previous_halt else None
            },

            "nextHalt": {

                "stationCode":
                    next_halt.get(
                        "stationCode"
                    ) if next_halt else None,

                "stationName":
                    next_halt.get(
                        "stationName"
                    ) if next_halt else None,

                "sequence":
                    next_halt.get(
                        "sequence"
                    ) if next_halt else None,

                "distance":
                    next_halt.get(
                        "distance"
                    ) if next_halt else None
            },

            "source": train_info.get(
                "source"
            ),

            "destination": train_info.get(
                "destination"
            ),

            "type": train_info.get(
                "type"
            ),

            "category": train_info.get(
                "category"
            ),

            "distance": train_info.get(
                "distance"
            ),

            "avgSpeed": train_info.get(
                "avgSpeed"
            ),

            "maxSpeed": train_info.get(
                "maxSpeed"
            ),

            "totalHalts": train_info.get(
                "totalHalts"
            ),

            "returnTrain": train_info.get(
                "returnTrain"
            ),

            "coachPosition": train_info.get(
                "coachPosition"
            ),

            "startDate":
                data.get("startDate"),

            "lastUpdatedAt":
                data.get("lastUpdatedAt")
        }

        return live_train

    except requests.exceptions.RequestException as e:

        print(
            f"RailRadar {train_number} "
            f"network error: {e}"
        )

        return None

    except ValueError as e:

        print(
            f"RailRadar {train_number} "
            f"JSON error: {e}"
        )

        return None

    except Exception as e:

        print(
            f"RailRadar {train_number} "
            f"unexpected error: {e}"
        )

        return None


# =========================================================
# RAILRADAR - MULTIPLE TRAINS
# =========================================================

def get_all_live_trains():

    live_trains = []

    for train_number in TRAIN_NUMBERS:

        train = get_live_train(
            train_number
        )

        if train:

            live_trains.append(train)

    print(
        "Total live trains received:",
        len(live_trains)
    )

    return live_trains


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
@login_required
def index():

    live_trains = get_all_live_trains()

    # First live train for backward compatibility
    live_data = None

    if live_trains:

        live_data = {
            "success": True,
            "data": live_trains[0]
        }

    return render_template(
        "index.html",
        trains=trains,
        assets=assets,
        live_data=live_data,
        live_trains=live_trains,
        result=None,
        ai_result=None
    )


# =========================================================
# ADD TRAIN
# =========================================================

@app.route(
    "/add_train",
    methods=["POST"]
)
@login_required
def add_train():

    train = {

        "train_number":
            request.form.get(
                "train_number"
            ),

        "train_name":
            request.form.get(
                "train_name"
            ),

        "section":
            request.form.get(
                "section"
            ),

        "start_time":
            int(
                request.form.get(
                    "start_time",
                    0
                )
            ),

        "end_time":
            int(
                request.form.get(
                    "end_time",
                    24
                )
            ),

        "priority":
            int(
                request.form.get(
                    "priority",
                    1
                )
            )
    }

    trains.append(train)

    return redirect(
        url_for("index")
    )


# =========================================================
# ADD ASSET
# =========================================================

@app.route(
    "/add_asset",
    methods=["POST"]
)
@login_required
def add_asset():

    asset = {

        "asset_name":
            request.form.get(
                "asset_name"
            ),

        "section":
            request.form.get(
                "section"
            ),

        "status":
            request.form.get(
                "status"
            )
    }

    assets.append(asset)

    return redirect(
        url_for("index")
    )


# =========================================================
# BLOCK PLANNER
# =========================================================

@app.route(
    "/plan",
    methods=["POST"]
)
@login_required
def plan():

    section = request.form.get(
        "section",
        "Bhopal-Itarsi"
    )

    duration = int(
        request.form.get(
            "duration",
            1
        )
    )

    # Simple block calculation
    # Later this can be replaced
    # by the actual AI optimizer.

    best_start = 1
    best_end = best_start + duration

    conflicts = 0

    for train in trains:

        if train["section"] != section:
            continue

        train_start = train["start_time"]
        train_end = train["end_time"]

        if (
            best_start < train_end
            and best_end > train_start
        ):
            conflicts += 1

    available_assets = len(
        [
            asset
            for asset in assets
            if asset["section"] == section
            and asset["status"] == "Available"
        ]
    )

    result = {

        "start_time":
            best_start,

        "end_time":
            best_end,

        "conflicts":
            conflicts,

        "available_assets":
            available_assets
    }

    # Simple AI score
    score = max(
        0,
        100
        - conflicts * 10
        + available_assets * 5
    )

    ai_result = {

        "start":
            best_start,

        "end":
            best_end,

        "conflicts":
            conflicts,

        "score":
            score
    }

    live_trains = get_all_live_trains()

    live_data = None

    if live_trains:

        live_data = {
            "success": True,
            "data": live_trains[0]
        }

    return render_template(
        "index.html",
        trains=trains,
        assets=assets,
        live_data=live_data,
        live_trains=live_trains,
        result=result,
        ai_result=ai_result
    )


# =========================================================
# LIVE API REFRESH
# =========================================================

@app.route(
    "/api/live-trains"
)
@login_required
def live_trains_api():

    live_trains = get_all_live_trains()

    return {
        "success": True,
        "count": len(live_trains),
        "trains": live_trains
    }


# =========================================================
# SINGLE TRAIN API
# =========================================================

@app.route(
    "/api/live-train/<train_number>"
)
@login_required
def single_live_train_api(
    train_number
):

    train = get_live_train(
        train_number
    )

    if not train:

        return {
            "success": False,
            "message": "Live train data unavailable",
            "trainNumber": train_number
        }, 404

    return {
        "success": True,
        "data": train
    }


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )