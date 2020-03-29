from pprint import pprint

import cv2
from PIL import Image

import module

TOTAL_WASH_TIME = 24  # total required time for waashing hands
STEP_WASH_SEC = 4  # required time(seconds) to wash for each step TOTAL_WASH_TIME / 6
STEP_PERCENT_ROUND = 2  # decimal points rounded up to
TIME_PER_STATUS = 0.8  # seconds, time per one element in status array


def get_frame_images():
    # Read the video from specified path
    cam = cv2.VideoCapture("static/demo.mp4")
    fps = cam.get(cv2.CAP_PROP_FPS)

    # frame
    imgs = []
    while (True):
        # reading from frame
        ret, frame = cam.read()
        if not ret:
            break
        imgs.append(Image.fromarray(frame))

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    return imgs, fps


def createJson(predicted, fps):
    TIME_PER_FRAME = 1 / fps
    STATUS_FRAME_CNT = TIME_PER_STATUS // TIME_PER_FRAME

    # variables initialization
    status = list()
    step_time = [0, ] * 6

    # parse the predicted data from model and create json for frontend
    len_predicted = len(predicted)
    for i, pred in enumerate(predicted):
        i += 1
        step_time[pred] += TIME_PER_FRAME

        # save to json every STATUS_FRAME_CNT frames
        if i % STATUS_FRAME_CNT == 0 or i == len_predicted - 1:
            total_time = i * TIME_PER_FRAME

            status.append({
                "current": pred,
                "steps": {
                    "time": [round(s, 2) for s in step_time],
                    "percent": [round((s / STEP_WASH_SEC) * 100, STEP_PERCENT_ROUND) for s in step_time]
                },
                "total": {
                    "time": total_time,
                    "percent": round((total_time / TOTAL_WASH_TIME) * 100)
                }
            })

    return {
        "time_per_status": TIME_PER_STATUS,
        "status": status
    }


def run():
    print("load images")
    imgs, fps = get_frame_images()

    print("predict labels")
    predicted = module.predict(imgs)

    print("Convert to json object")
    output = createJson(predicted, fps)
    pprint(output)

    return output
