#!/usr/bin/env python
from flask import Flask, render_template, Response
import picamera

app = Flask(__name__, static_url_path = "/image", static_folder="image")

@app.route('/')
def index():
    return render_template('index.html')

def cam_setup():
    cam = picamera.PiCamera()
    return cam

def gen(cam):
    while True:
        cam.capture('image.jpg')
        frame = open('image.jpg','rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(cam_setup()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
