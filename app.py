from flask import Flask, render_template, jsonify
from mcstatus import JavaServer

app = Flask(__name__)

# Our Minecraft Server Address and IP
SERVER_ADDRESS = "drake-efforts.tun.ply.gg"

# Logic
def get_server_status():
    try:
        server = JavaServer.lookup(SERVER_ADDRESS)
        status = server.status()

        return {
            "online": True,
            "players": status.players.online,
            "max_players": status.players.max,
            "version": status.version.name,
        }
    except Exception:
        return {
            "online": False,
            "players": 0,
            "max_players": 0,
            "version": "Unknown",
        }


# Website Stuff
@app.route("/")
def index():
    return render_template("index.html", status=get_server_status())


@app.route("/api/status")
def api_status():
    return jsonify(get_server_status())


# Backend stuff
if __name__ == "__main__":
    import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
