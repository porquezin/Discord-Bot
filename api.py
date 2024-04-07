from flask import Flask, request, jsonify, abort, render_template
from Classes import database

from utils.discordusername import get_discord_user_info


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scoreboard', methods=["GET"])
def scoreboard():
    db = database.Database()
    users_sorted = db.get_users_sorted_by_points()
    for user in users_sorted:
        user["name"] = get_discord_user_info(user["user_id"])
    return jsonify(users_sorted), 200


@app.route('/flag', methods=["GET", "POST"])
@app.route('/flag/<f>', methods=["GET", "DELETE"])
def flag(f=None):
    db = database.Database()

    if request.method == "GET":
        if f:
            flag = db.get_flag(f)
            if flag:
                return jsonify(flag), 200
            abort(404, "Flag not found")
        flags = db.get_all_flags()
        return jsonify(flags), 200

    elif request.method == "POST":
        data = request.get_json()
        flag = data.get("flag")
        points = data.get("points")

        if not flag or not points:
            abort(400, "Missing flag or points parameter")

        try:
            points = int(points)
        except ValueError:
            abort(400, "Points must be an integer")

        if db.add_flag(flag, points):
            return jsonify({"message": "Flag added successfully"}), 201
        abort(500,"Flag already exist.")
    elif request.method == "DELETE":
        if not f:
            abort(400, "Missing flag identifier")
        if db.delete_flag(f):
            return jsonify({"message": "Flag deleted successfully"}), 204
        abort(404, "Flag not found")


@app.route('/submit_flag', methods=["POST"])
def submit_flag():
    db = database.Database()
    data = request.get_json()
    user_id = data.get("user_id")
    flag = data.get("flag")
    db.add_user(user_id)

    if not user_id or not flag:
        abort(500, "Missing user_id or flag")

    flag_info = db.get_flag(flag)
    if not flag_info:
        abort(404, "Flag not found")

    success, points = db.add_user_flag(user_id, flag)
    if success:
        user = db.get_user_points(user_id)
        return jsonify({"message": "Flag submitted successfully", "points_awarded": points, "all_points": user}), 201
    abort(400, "Flag already submitted by this user.")


@app.route('/stop', methods=["GET"])
def stop():
    db = database.Database()
    if db.clear_tables():
        return "Stoped.", 200
    abort(500,"Error.")


if __name__ == '__main__':
    app.run(debug=False, host="127.0.0.1", port=5000)
