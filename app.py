from flask import Flask, render_template, jsonify
from mcstatus import JavaServer, BedrockServer

app = Flask(__name__)

# ==========================================
# SERVER CONFIGURATION / Our Main Server IP'S
# ==========================================
JAVA_IP = "drake-efforts.tun.ply.gg"
JAVA_PORT = 25565 # Default Port

BEDROCK_IP = "147.185.221.231"
BEDROCK_PORT = 57867
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    # --- JAVA STATUS ---
    java_data = {
        "online": False, "ping": None, "version": "Unknown",
        "players": 0, "max_players": 0, "player_names": []
    }
    try:
        java_server = JavaServer.lookup(f"{JAVA_IP}:{JAVA_PORT}")
        java_status = java_server.status()
        java_data["online"] = True
        java_data["ping"] = round(java_status.latency)
        java_data["version"] = java_status.version.name
        java_data["players"] = java_status.players.online
        java_data["max_players"] = java_status.players.max
        # Extract player names if available
        if java_status.players.sample:
            java_data["player_names"] = [p.name for p in java_status.players.sample]
    except Exception as e:
        print(f"Java Server Offline: {e}")

    # --- BEDROCK STATUS ---
    bedrock_data = {
        "online": False, "ping": None, "version": "Unknown"
    }
    try:
        bedrock_server = BedrockServer.lookup(f"{BEDROCK_IP}:{BEDROCK_PORT}")
        bedrock_status = bedrock_server.status()
        bedrock_data["online"] = True
        bedrock_data["ping"] = round(bedrock_status.latency)
        # Using .version instead of .name to fix the Bedrock bug
        bedrock_data["version"] = bedrock_status.version.version
    except Exception as e:
        print(f"Bedrock Server Offline: {e}")

    # Return as JSON API
    return jsonify({
        "java": java_data,
        "bedrock": bedrock_data
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)