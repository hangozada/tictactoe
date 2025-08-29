from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def main():
    data = {}
    print(request.remote_addr)
    return render_template("battleship.html.j2", **data)

@app.route("/move", methods=['POST'])
def move():
    receivedData = request.get_json(force=True)
    receivedMove = receivedData["move"]
    return {"data": "thank you", "player": request.remote_addr, "move": receivedMove}

@socketio.on('message')
def message(data):
    print(data)
    jsonData = {"data" : data}
    emit('receive_message', jsonData, broadcast=True)
    #emit({"data": "hello"}, json=True, broadcast=True)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    jsonData = {"move" : json["move"], "player": json["player"]}
    emit('receive_message', jsonData, broadcast=True)

@socketio.on('hit')
def handle_hit(hit):
    print('received hit: ' + str(hit))
    jsonData = {"hit" : True, "player": hit["player"], "move": hit["move"]}
    emit('receive_message', jsonData, broadcast=True)

@app.route("/salma")
def salma():
    data = {}
    return render_template("salma.html", **data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8888")
    #socketio.run(app)