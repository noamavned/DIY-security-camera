import time
import cv2
import numpy as np
from PIL import Image
import io
import requests


start = time.time()


def sendTel(frame, text="Cam caught something!"):
    if (time.time()-start < 5):
        return
    token = "5989215470:AAEXIwnrG-dnquwBe6f-6Yjmp4SBKsgZah4"
    chat_id = "5659362290"
    url_req = f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}"
    color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(color_coverted)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    files = {"photo": img_bytes}
    results = requests.post(url_req, files=files)


cap = cv2.VideoCapture(0)
last_mean = 0
detected_motion = False
frame_rec_count = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')

while (True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = np.abs(np.mean(gray) - last_mean)
    last_mean = np.mean(gray)
    if result > 0.3:
        detected_motion = True
        sendTel(frame)
    if detected_motion:
        frame_rec_count = frame_rec_count + 1
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
