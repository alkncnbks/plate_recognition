import cv2
import pytesseract
import numpy as np
import csv
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://plate-23e2a-default-rtdb.firebaseio.com/'
})

def log_plaka(plaka):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("plaka_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([now, plaka])

def firebase_log(plaka):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ref = db.reference('plaka_kayitlari')
    ref.push({
        'tarih_saat': now,
        'plaka': plaka
    })


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    if coords.shape[0] == 0:
        return image
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(c)
            padding = 15
            x = max(x - padding, 0)
            y = max(y - padding, 0)
            w = min(w + 2 * padding, frame.shape[1] - x)
            h = min(h + 2 * padding, frame.shape[0] - y)

            plate = frame[y:y+h, x:x+w]
            plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
            plate_gray = cv2.resize(plate_gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            plate_gray = cv2.bilateralFilter(plate_gray, 11, 17, 17)
            plate_gray = cv2.adaptiveThreshold(plate_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, 11, 2)

            plate_deskewed = deskew(plate_gray)

            config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            text = pytesseract.image_to_string(plate_deskewed, config=config).strip().replace(" ", "").replace("\n", "")

            if text and len(text) >= 5:
                print("📘 Okunan Plaka:", text)
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
                log_plaka(text)
                firebase_log(text)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            break

    cv2.imshow("Plaka Tanıma Sistemi", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
