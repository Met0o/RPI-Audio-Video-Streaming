# sudo apt-get install portaudio19-dev
# pip install pyaudio Flask Flask-SocketIO cv2 numpy
import cv2
import pyaudio
import numpy as np
from flask import Flask, Response, render_template
from flask_socketio import SocketIO, emit

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

app = Flask(__name__)
socketio = SocketIO(app)

def stream_audio():
    while True:
        data = stream.read(CHUNK)
        socketio.emit('audio', np.frombuffer(data, dtype=np.int16).tolist())

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.start_background_task(stream_audio)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def generate_frames():

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FPS, 25)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
            ret, buffer = cv2.imencode('.jpg', frame, encode_param)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():

    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000)