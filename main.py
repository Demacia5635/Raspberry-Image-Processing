import cv2
from flask import Flask, Response
import networktables_handler
import processing
from numpy import ndarray
from threading import Thread

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen_frames() -> None:
    frame : ndarray = None
    while True:

        success, frame = camera.read()
        if not success:
            break

        processing.process_image(frame.copy())

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

@app.route('/')
def videofeed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def update_camera_settings() -> None:
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, networktables_handler.camera_height)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, networktables_handler.camera_width)
    camera.set(cv2.CAP_PROP_FPS, networktables_handler.camera_fps)

def start():
    print('starting...')
    while True:
        cap = cv2.VideoCapture('http://localhost:8081')
        if cap.read()[0]:
            cap.release()
            break
    print('Started!')

if __name__ == "__main__":
    if networktables_handler.connected_to_robot():
        networktables_handler.connect()
    update_camera_settings()
    thread = Thread(target=start)
    thread.start()

    app.run(port=8081, host='0.0.0.0')