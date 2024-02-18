import time
import keyboard
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')

@app.route("/")
def hello_world():
    return render_template("page.html")

@socketio.on("hello")
def sock_hello(data):
    print("hello ", data)

@socketio.on("click")
def sock_click(data):
    keyboard.press_and_release(data.get("action"))
    print("pressed ", data)



if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0")