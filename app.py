from flask import Flask, render_template, jsonify
from mcstatus import JavaServer, BedrockServer

app = Flask(__name__)

# Minecraft Server Addresses
JAVA_ADDRESS = "drake-efforts.tun.ply.gg"
BEDROCK_ADDRESS = "147.185.221.231:57867"


# Java Server Status
def get_java_status():
    try:
        server = JavaServer.lookup(JAVA_ADDRESS)
        status = server.status()

        players = []

        if status.players.sample:
            players = [
                player.name
                for player in status.players.sample
            ]

        return {
            "online": True,
            "players": status.players.online,
            "max_players": status.players.max,
            "version": status.version.name,
            "ping": round(status.latency),
            "player_names": players
        }

    except Exception:
        return {
            "online": False,
            "players": 0,
            "max_players": 0,
            "version": "Unknown",
            "ping": None,
            "player_names": []
        }


# Bedrock Server Status
def get_bedrock_status():
    try:
        server = BedrockServer.lookup(BEDROCK_ADDRESS)
        status = server.status()

        return {
            "online": True,
            "players": status.players.online,
            "max_players": status.players.max,
            "version": status.version.name,
            "ping": round(status.latency)
        }

    except Exception:
        return {
            "online": False,
            "players": 0,
            "max_players": 0,
            "version": "Unknown",
            "ping": None
        }


# Get Both Server Statuses
def get_server_status():
    return {
        "java": get_java_status(),
        "bedrock": get_bedrock_status()
    }


# Website 
@app.route("/")
def index():
    return render_template("index.html", status=get_server_status())


@app.route("/api/status")
def api_status():
    return jsonify(get_server_status())


# Backend
if __name__ == "__main__":
    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )