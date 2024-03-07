from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import json
import keyboard
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
profiles = json.load(open("profiles.json"))


@app.route("/")
def index_route():
    return render_template("index.html")


@socketio.on("fetch_profiles_data")
def sock_fetch_profiles_data():
    socketio.emit("profiles", json.load(open("profiles.json")))
    
@socketio.on("click")
def sock_on_button_press(data):
    profiles = json.load(open("profiles.json"))


    profile = data["profile"]
    button = data["button"]
    mapping = profiles["profiles"][profile]["mappings"].get(str(button))


    if mapping != None:
        keyboard.press(mapping.get("action"))
        time.sleep(0.1)
        keyboard.release(mapping.get("action"))


if __name__ == "__main__":
    config = json.load(open("config.json"))
    socketio.run(app, host=config["webserver_host"], port=config["webserver_port"])         
    