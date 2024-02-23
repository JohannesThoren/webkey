import keyboard
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
from time import sleep

app = Flask(__name__)
socketio = SocketIO(app, debug=True, cors_allowed_origins="*")


@app.route("/")
def route_index():
    return render_template("page.html")


@socketio.on("click")
def sock_click(data):
    keyboard.press(data.get("action"))
    app.logger.info("button pressed %s", data)
    sleep(0.1)
    keyboard.release(data.get("action"))
    app.logger.info("button released %s", data)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
