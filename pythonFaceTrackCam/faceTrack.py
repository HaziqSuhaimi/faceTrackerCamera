import cv2
import numpy as np
import serial    #pyserial

arduino = serial.Serial('COM5', 115200, timeout=.1)

cap = cv2.VideoCapture(1)# 1 because 0 is the built in camera
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  #pilih la classifier korang sendiri.. aku pilih yg bisye2 je
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # data = arduino.readline()[:-2] #check arduino serial
    # if data:
    #     print(data)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    height, width = frame.shape[:2]
    mid_H = int(np.floor(height/2))
    mid_W = int(np.floor(width/2))

    cv2.line(frame, (0, mid_H), (width, mid_H), (0, 200, 0), 1)
    cv2.line(frame, (mid_W, 0), (mid_W, height), (0, 200, 0), 1)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 0), 1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        mid_face_H = int(np.floor(y+(h/2)))
        mid_face_W = int(np.floor(x+(w/2)))

        dist_H = mid_H - mid_face_H
        dist_W = mid_W - mid_face_W

        cv2.line(frame, (x, mid_H), (x, mid_face_H), (0, 0, 200), 1)
        cv2.line(frame, (mid_W, y), (mid_face_W, y), (0, 0, 200), 1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(dist_H), (x, mid_H), font,
                    1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str(dist_W), (mid_W, y), font,
                    1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.line(frame, (x, mid_face_H), (x+w, mid_face_H), (0, 200, 0), 1)
        cv2.line(frame, (mid_face_W, y), (mid_face_W, y+h), (0, 200, 0), 1)

        if (dist_W < 0):
            arduino.write(b'R')
            print("right")
        elif (dist_W > 0):
            arduino.write(b'L')
            print("left")
        else:
            arduino.write(b'C')
            print("center")

        if (dist_H < 0):
            arduino.write(b'B')
            print("bawah")
        elif (dist_H > 0):
            arduino.write(b'A')
            print("atas")
        else:
            arduino.write(b'T')
            print("center")

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
