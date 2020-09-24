

import cv2
import numpy as np
global sayac
sayac = 0


backsub = cv2.createBackgroundSubtractorMOG2(varThreshold=200, detectShadows=False)
capture = cv2.VideoCapture("rtsp://s14.us-east-1.skyvdn.com:1935/rtplive/HamptonRoads851")

frame_width = int(capture.get(3))
frame_height = int(capture.get(4))

fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
kayit = cv2.VideoWriter('kayit.264', fourcc, 10, (frame_width, frame_height))

if capture:
    while True:
        ret, frame = capture.read()

        if ret:
            fgmask = backsub.apply(frame)

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
            kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)


            line1 = cv2.line(frame, (70, 160), (240, 160), (0, 255, 0), 2)
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            fgmask = cv2.dilate(fgmask, kernel2, iterations=1)
            _,contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            try:
                hierarchy = hierarchy[0]
            except:
                hierarchy = []
            for contour, hier, in zip(contours, hierarchy):
                (x, y, w, h) = cv2.boundingRect(contour)
                if w > 18 and h > 18:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    a = int(w / 2)
                    b = int(h / 2)
                    marker = cv2.drawMarker(frame, (x + a, y + b), (0, 255, 0), markerType=50, markerSize=15)

                    if 70 < x + a < 240 and 155 < y + b < 162:
                        sayac += 1
                        print(sayac)


            cv2.putText(frame, "Araba: " + str(sayac), (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            kayit.write(frame)
            cv2.imshow("Takip", frame)
            cv2.imshow("Arka Plan Cıkar", fgmask)

        key = cv2.waitKey(60)
        if key == ord('q'):
            break
kayit.release()
capture.release()

cv2.destroyAllWindows()

