from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    # 获取页面
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    # connect是事件名，namespace是命名空间
    print('建立连接...connect')


@socketio.on('timer', namespace='/test')
def sync_time(message):
    # time 是另一个事件，这里返回当前时间字符串
    from datetime import datetime
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emit('timer', {'data': now_str})


@socketio.on('my event', namespace='/test')
def test_message(message):
    # my event事件 将client发送过来的信息原路返回
    print('get message', message['data'])
    emit('my event', {'data': message['data']})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('断开连接...disconnect')


if __name__ == '__main__':
    socketio.run(app, debug=True)
