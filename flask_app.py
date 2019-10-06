''' Flask app to run the sudoku solver on Azure Web Apps'''

# Currently used imports
from flask import Flask, make_response, render_template, Response
from imutils.video import VideoStream
import threading
import imutils
import numpy as np
import cv2
import time
import transform as tf 

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

# Instantiate app
app = Flask(__name__)

# Initialise the video stream and give camera time to warm up
vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")


def get_frame():
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock

	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
	
		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
        
if __name__ == "__main__":
	
	# start a thread that will perform video reading detection
	# t = threading.Thread(target=get_frame)
	# t.daemon = True
	# t.start()

    app.run(debug=True, threaded=True, use_reloader=False)

vs.stop()
