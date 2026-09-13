from flask import Flask, render_template, request, redirect, session
from ai_planner import ai_recommendation

from database import init_database, get_connection
from planner import find_best_block, format_time

app = Flask(__name__)
app.secret_key = "railway-block-planner-secret-key"

# Initialize database
init_database()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        department = request.form["department"]

        conn = get_connection()

        user = conn.execute("""
            SELECT * FROM users
            WHERE user_id = ?
            AND department = ?
        """, (user_id, department)).fetchone()

        conn.close()

        if user and password == user["password_hash"]:
            session["user_id"] = user_id
            session["department"] = department
            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid User ID, Password or Department"
        )

    return render_template("login.html")



@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_connection()

    trains = conn.execute("""
        SELECT * FROM trains
        ORDER BY start_time
    """).fetchall()

    assets = conn.execute("""
        SELECT * FROM assets
        ORDER BY id
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        trains=trains,
        assets=assets,
        result=None,
        ai_result=None
    )


@app.route("/add_train", methods=["POST"])
def add_train():
    train_number = request.form["train_number"]
    train_name = request.form["train_name"]
    section = request.form["section"]
    start_time = int(request.form["start_time"])
    end_time = int(request.form["end_time"])
    priority = int(request.form["priority"])

    conn = get_connection()

    conn.execute("""
        INSERT INTO trains
        (train_number, train_name, section, start_time, end_time, priority)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        train_number,
        train_name,
        section,
        start_time,
        end_time,
        priority
    ))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/add_asset", methods=["POST"])
def add_asset():
    asset_name = request.form["asset_name"]
    section = request.form["section"]
    status = request.form["status"]

    conn = get_connection()

    conn.execute("""
        INSERT INTO assets
        (asset_name, section, status)
        VALUES (?, ?, ?)
    """, (
        asset_name,
        section,
        status
    ))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/plan", methods=["POST"])
def plan():
    section = request.form["section"]
    duration = int(request.form["duration"])

    conn = get_connection()

    trains = conn.execute("""
        SELECT * FROM trains
        WHERE section = ?
    """, (section,)).fetchall()

    assets = conn.execute("""
        SELECT * FROM assets
        WHERE section = ?
    """, (section,)).fetchall()

    # Normal planner
    result = find_best_block(
        trains,
        section,
        duration
    )

    # Available assets
    result["available_assets"] = sum(
        1 for asset in assets
        if asset["status"].lower() == "available"
    )

    # AI recommendation
    ai_result = ai_recommendation(
        trains,
        assets,
        section,
        duration
    )

    conn.close()

    # Format normal planner result
    result["start_time"] = format_time(
        result["start"]
    )

    result["end_time"] = format_time(
        result["end"]
    )

    return render_template(
        "index.html",
        trains=trains,
        assets=assets,
        result=result,
        ai_result=ai_result
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )