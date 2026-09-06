from flask import Flask, render_template, jsonify
from mcstatus import JavaServer, BedrockServer
import os

app = Flask(__name__)

# ==========================================
# SERVER ADDRESSES
# ==========================================
JAVA_ADDRESS = "drake-efforts.tun.ply.gg"
BEDROCK_ADDRESS = "147.185.221.231:57867"

def get_java_status():
    try:
        server = JavaServer.lookup(JAVA_ADDRESS)
        status = server.status()

        players = []
        if status.players.sample:
            players = [p.name for p in status.players.sample]

        return {
            "online": True,
            "players": status.players.online,
            "max_players": status.players.max,
            "version": status.version.name,
            "ping": round(status.latency),
            "player_names": players
        }
    except Exception as e:
        print(f"Java Server Offline: {e}")
        return {
            "online": False,
            "players": 0,
            "max_players": 0,
            "version": "Unknown",
            "ping": None,
            "player_names": []
        }

def get_bedrock_status():
    try:
        server = BedrockServer.lookup(BEDROCK_ADDRESS)
        status = server.status()
        
        # Safely extract Bedrock version to prevent AttributeErrors
        version_name = "Unknown"
        if hasattr(status, 'version'):
            if hasattr(status.version, 'version'):
                version_name = status.version.version
            elif hasattr(status.version, 'name'):
                version_name = status.version.name
            else:
                version_name = str(status.version)

        return {
            "online": True,
            "ping": round(status.latency),
            "version": version_name
        }
    except Exception as e:
        print(f"Bedrock Server Offline: {e}")
        return {
            "online": False,
            "ping": None,
            "version": "Unknown"
        }

# ==========================================
# ROUTES
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    # Wrap the entire response in a try-except block. 
    # This guarantees the API will ALWAYS return valid JSON and never crash the UI.
    try:
        return jsonify({
            "java": get_java_status(),
            "bedrock": get_bedrock_status()
        })
    except Exception as e:
        print(f"FATAL API ERROR: {e}")
        return jsonify({
            "java": {"online": False, "players": 0, "max_players": 0, "version": "Error", "ping": None, "player_names": []},
            "bedrock": {"online": False, "ping": None, "version": "Error"}
        })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )