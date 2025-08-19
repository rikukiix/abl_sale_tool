# --- minimal_test.py (多线程版本) ---

# 【移除】不再需要 eventlet
# import eventlet
# eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key_for_test'

# 【核心改动 1】不再指定 async_mode，让 Flask-SocketIO 自动选择最佳模式
# 在没有 eventlet/gevent 的情况下，它会自动选择 'threading'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    print("--- MINIMAL TEST (Threading): HTTP / route was hit! ---")
    return "Minimal Flask App is running in Threading mode."

# 【核心改动 2】所有事件处理器保持不变，它们是通用的
@socketio.on('connect', namespace='/sale')
def handle_connect():
    sid = request.sid
    print(f"--- MINIMAL TEST (Threading): Client connected! SID: {sid}")
    emit('connection_successful', {'message': f'Welcome, your SID is {sid}'})

@socketio.on('ping_test', namespace='/sale')
def handle_ping_test(data):
    sid = request.sid
    print(f"--- MINIMAL TEST (Threading): Received 'ping_test' from SID {sid}. Data: {data}")
    emit('pong_test', {'message': 'Pong from minimal test app!'})

@socketio.on('disconnect', namespace='/sale')
def handle_disconnect():
    sid = request.sid
    print(f"--- MINIMAL TEST (Threading): Client disconnected. SID: {sid}")

if __name__ == '__main__':
    print("--- Starting Minimal Flask-SocketIO Test Server (Threading Mode) ---")
    # 【核心改动 3】直接使用 socketio.run() 启动，它会自动使用 Werkzeug 的多线程服务器
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)