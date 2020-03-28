from flask import Flask, render_template, request
import cv2
import os
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # pass
        return 'hello'
    else:
        return render_template('lahacks.html')

def FrameCapture():
    # Read the video from specified path
    cam = cv2.VideoCapture("static/hand.mp4")

    try:
        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')

    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of data')

    # frame
    imgs = []

    while (True):

        # reading from frame
        ret, frame = cam.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgs.append(Image.fromarray(frame))

        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)




