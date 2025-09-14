import cv2
import easyocr
import json
import os

class BusImageDetector:
    def __init__(self, bus_data_file="bus_data.json"):
        self.reader = easyocr.Reader(['en'])
        if not os.path.exists(bus_data_file):
            raise FileNotFoundError(f"{bus_data_file} not found!")
        with open(bus_data_file, "r", encoding="utf-8") as f:
            self.bus_data = json.load(f)

    def detect_from_image(self, image_path: str) -> str:
        if not os.path.exists(image_path):
            return "Boss, এই image path টা পাচ্ছি না!"

        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return "Boss, image খুলতে problem হচ্ছে!"

        # OCR
        results = self.reader.readtext(img)

        detected_number = None
        for (_, text, prob) in results:
            if prob > 0.4:
                text_clean = text.strip().upper()
                # Check if the text is a bus number
                if text_clean in self.bus_data:
                    detected_number = text_clean
                    break

        if detected_number:
            bus_info = self.bus_data[detected_number]
            return (
                f"Boss, ami detect korechi Bus No. {detected_number} — "
                f"{bus_info['name']}. Eta jachhe: {bus_info['route']}."
            )
        else:
            return "Boss, bus detect korte perechi, কিন্তু number database এ নেই অথবা pora gelo na."
