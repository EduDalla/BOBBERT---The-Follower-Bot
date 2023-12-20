import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()

    if success:
        img = cv2.flip(img, 1)  # Flip the captured frame horizontally

        border_img = np.zeros_like(img)
        border_color = (255, 255, 0)
        border_img[:, :] = border_color

        img = cv2.resize(img, (border_img.shape[1] - 20, border_img.shape[0] - 20))
        border_img[10:-10, 10:-10] = img

        overlay_img = cv2.imread('C:\\Users\\eduar\\Downloads\\Group_12-removebg-preview.png')
        overlay_img = cv2.resize(overlay_img, (100, 100))

        x_offset = border_img.shape[1] - overlay_img.shape[1] - 10
        y_offset = 10
        border_img[y_offset:y_offset + overlay_img.shape[0], x_offset:x_offset + overlay_img.shape[1]] = overlay_img

        cv2.imshow("Image", border_img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


