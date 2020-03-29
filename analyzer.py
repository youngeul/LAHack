from pprint import pprint

import cv2
from PIL import Image

import module

from flask import send_file

TOTAL_WASH_TIME = 24  # total required time for waashing hands
STEP_WASH_SEC = 4  # required time(seconds) to wash for each step TOTAL_WASH_TIME / 6
STEP_PERCENT_ROUND = 2  # decimal points rounded up to
TIME_PER_STATUS = 0.2  # seconds, time per one element in status array


def get_frame_images():
    # Read the video from specified path
    cam = cv2.VideoCapture("static/demo_modified.mp4")
    fps = cam.get(cv2.CAP_PROP_FPS)

    # frame
    imgs = []
    idx = 0
    while (True):
        # reading from frame
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imwrite(f'static/frame/frame_{idx}.jpg', frame)
        imgs.append(Image.fromarray(frame))
        idx += 1

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
    idxs = [0, ] * 6

    # parse the predicted data from model and create json for frontend
    len_predicted = len(predicted)
    for i, pred in enumerate(predicted):
        i += 1
        idxs[pred] += 1

        # save to json every STATUS_FRAME_CNT frames
        if i % STATUS_FRAME_CNT == 0 or i == len_predicted - 1:
            total_time = i * TIME_PER_FRAME

            max_cnt = max(idxs)
            max_idxs = [i for i, c in enumerate(idxs) if c == max_cnt][0]
            step_time[max_idxs] += TIME_PER_STATUS
            idxs = [0, ] * 6

            status.append({
                "current": max_idxs,
                "idx": i-1,
                "steps": {
                    "time": [round(s, 2) for s in step_time],
                    "percent": [min(1., s / STEP_WASH_SEC) for s in step_time]
                },
                "total": {
                    "time": round(total_time),
                    "percent": sum([min(1., s / STEP_WASH_SEC) for s in step_time]) / 6
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
    # pprint(output)

    return output
