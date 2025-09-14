# daku_bus_detector.py
import cv2
import easyocr
import json
import os
import time

class DakuBusDetector:
    def __init__(self, camera_index=0, bus_db="bus_data.json"):
        self.camera_index = camera_index
        self.bus_db = bus_db
        self.reader = easyocr.Reader(["en"], gpu=False)
        self.bus_data = self.load_bus_data()

    def load_bus_data(self):
        if not os.path.exists(self.bus_db):
            return {}
        with open(self.bus_db, "r", encoding="utf-8") as f:
            return json.load(f)

    def detect_bus(self):
        cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            return "[ERROR] Camera খুলতে পারছি না। নিশ্চিত করুন যে OBS Virtual Camera চালু আছে।"

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return "[ERROR] Frame নিতে ব্যর্থ।"

        results = self.reader.readtext(frame)
        detected_info = []

        for (_, text, _) in results:
            bus_no = text.strip()
            if bus_no in self.bus_data:
                bus_info = self.bus_data[bus_no]
                detected_info.append(
                    f"🚍 {bus_info['name']} (Bus {bus_no}) — Route: {bus_info['route']}"
                )

        if detected_info:
            filename = f"detected_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            return "\n".join(detected_info) + f"\n[INFO] Frame saved as {filename}"
        else:
            return "[INFO] কোনো bus detect করা যায়নি।"
