# daku_bus_tool.py
import cv2
import easyocr
import json
import os
import asyncio

# Load bus database
def load_bus_data(bus_db="bus_data.json"):
    if not os.path.exists(bus_db):
        return {}
    with open(bus_db, "r", encoding="utf-8") as f:
        return json.load(f)

# Bus detection function (synchronous)
def detect_bus(camera_index=1):
    bus_data = load_bus_data()
    reader = easyocr.Reader(["en"], gpu=False)

    cap = cv2.VideoCapture(camera_index)

    if cap is None or not cap.isOpened():
        return "[ERROR] কোনো camera detect করা যায়নি। OBS Virtual Camera চালু করুন।"

    ret, frame = cap.read()
    if not ret:
        cap.release()
        return "[ERROR] Frame নিতে ব্যর্থ।"

    detected_info = []

    results = reader.readtext(frame)
    for (_, text, _) in results:
        bus_no = text.strip()
        if bus_no in bus_data:
            bus_info = bus_data[bus_no]
            detected_info.append(
                f"🚍 {bus_info['name']} (Bus {bus_no}) — Route: {bus_info['route']}"
            )

    cap.release()
    cv2.destroyAllWindows()

    if detected_info:
        return "\n".join(detected_info)
    else:
        return "[INFO] কোনো bus detect করা যায়নি।"
