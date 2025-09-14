import cv2
import easyocr
import json
import os

# Bus Database Loader
def load_bus_data(bus_db="bus_data.json"):
    if not os.path.exists(bus_db):
        return {}
    with open(bus_db, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_bus_from_camera():
    bus_data = load_bus_data()
    reader = easyocr.Reader(["en"], gpu=False)

   
    cap = cv2.VideoCapture(1)
        

    if cap is None:
        print("[ERROR] কোনো camera detect করা যায়নি। OBS Virtual Camera চালু করুন।")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Frame নিতে ব্যর্থ।")
            break

        # OCR
        results = reader.readtext(frame)
        detected_info = []

        for (_, text, _) in results:
            bus_no = text.strip()
            if bus_no in bus_data:
                bus_info = bus_data[bus_no]
                detected_info.append(
                    f"🚍 {bus_info['name']} (Bus {bus_no}) — Route: {bus_info['route']}"
                )
                cv2.putText(
                    frame,
                    f"{bus_info['name']} ({bus_no})",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

        # Show results
        if detected_info:
            print("\n".join(detected_info))
        else:
            print("[INFO] কোনো bus detect করা যায়নি।")

        # Show camera feed
        cv2.imshow("OBS Virtual Camera - Bus Detection", frame)

        # Quit with Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_bus_from_camera()
