import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    cv2.waitKey(1)

