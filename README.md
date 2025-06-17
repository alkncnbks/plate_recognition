# License Plate Recognition System using OpenCV, OCR and Firebase

This project is developed as a part of a university graduation project.  
The system automatically detects and recognizes license plates from a live camera feed, logs the recognized plates both locally and to a Firebase Realtime Database.

---

#Technologies Used**

- Python 3.x
- OpenCV (Image Processing)
- Tesseract OCR (Optical Character Recognition)
- Firebase Realtime Database (Cloud Data Storage)
- NumPy
- CSV File Logging

---

#Project Purpose**

- Automatically detect vehicle license plates using computer vision.
- Recognize the plate characters with OCR.
- Log recognized plates into:
  - Local CSV file for backup.
  - Firebase Realtime Database for cloud access.
- Build a real-time system capable of live recognition.

---

#System Architecture**

1. **Camera Input**  
   Live video stream captured from camera.

2. **Preprocessing**  
   Image filtering, edge detection, contour detection.

3. **License Plate Detection**  
   Plate region extracted using contour approximation.

4. **Deskewing**  
   Plate image rotation correction to improve OCR accuracy.

5. **OCR Recognition**  
   Plate text is recognized using Tesseract OCR.

6. **Logging**  
   - Recognized plate is saved into a local CSV file.
   - The same data is also pushed to Firebase Realtime Database.

---

#Project Directory Structure**

#Create and activate virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate

#Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt

#Install Tesseract OCR:

bash
Copy
Edit
brew install tesseract

#Setup Firebase:

Create a Firebase Project.

Enable Realtime Database.

Download serviceAccountKey.json and place it in the project folder.

Update your databaseURL inside plaka_recognition_firebase.py.

#How to Run the Project
bash
Copy
Edit
python plaka_okuma_firebase.py
The system will open the live camera feed.

Detected plates will be displayed on screen, logged locally and uploaded to Firebase.

⚠ Important Notes
Make sure serviceAccountKey.json is NOT uploaded to public repositories.

The system works best with license plates that are:

Well lit

Front-facing

Not blurry

#Possible Improvements
YOLO based plate detection for higher accuracy.

Deep Learning OCR models instead of classical Tesseract.

Character segmentation for increased recognition success.

Web dashboard integration to monitor Firebase logs.

#Prepared for: Graduation Project
By Alkan Canbakış & Emrah Daniş,
Computer Engineering Department
Beykent University

