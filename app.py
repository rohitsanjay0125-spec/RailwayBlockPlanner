from flask import Flask, render_template, request

from database import init_database, get_connection
from planner import find_best_block, format_time

app = Flask(__name__)

init_database()


@app.route("/")
def home():
    conn = get_connection()

    trains = conn.execute(
        "SELECT * FROM trains ORDER BY start_time"
    ).fetchall()

    assets = conn.execute(
        "SELECT * FROM assets"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        trains=trains,
        assets=assets,
        result=None
    )


@app.route("/plan", methods=["POST"])
def plan():
    section = request.form["section"]
    duration = int(request.form["duration"])

    conn = get_connection()

    trains = conn.execute(
        "SELECT * FROM trains WHERE section = ?",
        (section,)
    ).fetchall()

    assets = conn.execute(
        "SELECT * FROM assets WHERE section = ?",
        (section,)
    ).fetchall()

    result = find_best_block(
        trains,
        section,
        duration
    )

    conn.close()

    result["start_time"] = format_time(result["start"])
    result["end_time"] = format_time(result["end"])

    return render_template(
        "index.html",
        trains=trains,
        assets=assets,
        result=result
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)