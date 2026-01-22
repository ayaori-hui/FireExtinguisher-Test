import cv2
import json
import os
from ultralytics import YOLO

# 🔹 현재 py 파일 위치 기준
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔹 config.json 절대경로
config_path = os.path.join(BASE_DIR, "config", "config.json")

# 🔹 JSON 파일 읽기 (★ 여기 중요)
with open(config_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

# 🔹 모델 경로도 python 기준으로
model_path = os.path.join(BASE_DIR, "model", "best.pt")

webcam_index = cfg["webcam_index"]
CONF_TH = cfg["confidence_threshold"]
REQUIRED_FRAMES = cfg["required_frames"]

# 🔹 YOLO 모델 로드
model = YOLO(model_path)

cap = cv2.VideoCapture(webcam_index)
detected_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    frame_detected = False

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])
            if conf < CONF_TH:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls = int(box.cls[0])
            label = r.names[cls]

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            print(f"🔥 소화기 감지 | x={cx}, y={cy}, conf={conf:.2f}")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
            cv2.putText(
                frame,
                f"{label} {conf:.2f} ({cx},{cy})",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            frame_detected = True

    if frame_detected:
        detected_frames += 1
    else:
        detected_frames = 0

    if detected_frames >= REQUIRED_FRAMES:
        print("✅ 소화기 확실히 감지됨")

    cv2.imshow("Webcam Fire Extinguisher Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
