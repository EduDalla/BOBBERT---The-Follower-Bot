"""

Pose Module 

By: Computer Vision Zone 

Website: https://www.computervision.zone/ 
"""

import cv2
import mediapipe as mp
import math
import serial
import time


class PoseDetector:
    """ 
    Estimates Pose points of a human body using the mediapipe library. 
    """

    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        """ 
        :param mode: In static mode, detection is done on each image: slower 
        :param upBody: Upper boy only flag 
        :param smooth: Smoothness Flag 
        :param detectionCon: Minimum Detection Confidence Threshold 
        :param trackCon: Minimum Tracking Confidence Threshold 
        """
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

    def findPose(self, img, draw=True):
        """ 
        Find the pose landmarks in an Image of BGR color space. 
        :param img: Image to find the pose in. 
        :param draw: Flag to draw the output on the image. 
        :return: Image with or without drawings 
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
                )
        return img

    def findPosition(self, img, draw=True, bboxWithHands=False):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                self.lmList.append([id, cx, cy, cz])

                # Bounding Box
            ad = abs(self.lmList[12][1] - self.lmList[11][1]) // 2
            if bboxWithHands:
                x1 = self.lmList[16][1] - ad
                x2 = self.lmList[15][1] + ad
            else:
                x1 = self.lmList[12][1] - ad
                x2 = self.lmList[11][1] + ad

            y2 = self.lmList[29][2] + ad
            y1 = self.lmList[1][2] - ad
            bbox = (x1, y1, x2 - x1, y2 - y1)
            cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + bbox[3] // 2

            bboxInfo = {"bbox": bbox, "center": (cx, cy)}

            if draw:
                cv2.rectangle(img, bbox, (255, 0, 0), 3)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            return self.lmList, bboxInfo
        else:
            return [], {}

    def findAngle(self, img, p1, p2, p3, draw=True):
        """ 
        Finds angle between three points. Inputs index values of landmarks 
        instead of the actual points. 
        :param img: Image to draw output on. 
        :param p1: Point1 - Index of Landmark 1. 
        :param p2: Point2 - Index of Landmark 2.
        :param p3: Point3 - Index of Landmark 3. 
        :param draw: Flag to draw the output on the image. 
        :return: 
        """
        # Get the landmarks
        # print(self.lmList[p1][1:])
        # print(self.lmList[p2][1:])
        # print(self.lmList[p3][1:])

        x1 = self.lmList[p1][1]
        x2 = self.lmList[p2][1]
        x3 = self.lmList[p3][1]

        y1 = self.lmList[p1][2]
        y2 = self.lmList[p2][2]
        y3 = self.lmList[p3][2]

        # Calculate the Angle 
        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        )
        if angle < 0:
            angle += 360

            # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 0, 0), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(
                img, str(int(angle)), (x2 - 50, y2 + 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2
            )

        return angle

    # def encontrarangulos(pontos):


#             # BDA BDB BEA  BEB  PDA  PDB  PEA  PEB
#     angles = [0,  0,   0,   0,   0,   0,   0,   0]

#  # Angulo BDA =
#     p14x = 0
#     p12y = 0
#     p12x = pontos[12][1] - pontos[14][1]
#     p14y = pontos[14][2] - pontos[12][2]
#     p1bdax = p12x
#     p1bday = p14y

#     if p1bda != 0:
#         angles[0] = (math.atan(p14y / p1bdax) * 180) + 360

#     print(angles)


#  # Angulo BDB =

#     p16x = 0
#     p14y = 0
#     p14x = pontos[14][1] - pontos[16][1]
#     p16y = pontos[16][2] - pontos[14][2]
#     p1bdbx = p14x
#     p1bdby = p16y

#     if p1bdb != 0:
#         angles[0] = (math.atan(p16y / p1bdbx) * 180) + 360

#     print(angles)


#  # Angulo BEA =
#     p13x = 0
#     p11y = 0
#     p11x = pontos[11][1] - pontos[13][1]
#     p13y = pontos[13][2] - pontos[11][2]
#     p1bebx = p11x
#     p1beby = p13y

#     if p1beb != 0:
#         angles[0] = ((math.atan(p13y / p1bebx) * 180) + 360)

#     print(angles)

#  # Angulo BEB =

#     p15x = 0
#     p13y = 0
#     p13x = pontos[13][1] - pontos[15][1]
#     p15y = pontos[15][2] - pontos[13][2]
#     p1bebx = p13x
#     p1beby = p15y

#     if p1beb != 0:
#         angles[0] = (math.atan(p15y / p1bebx) * 180) + 360

#     print(angles)


#  # Angulo PDA =

#     p26x = 0
#     p24y = 0
#     p24x = pontos[24][1] - pontos[26][1]
#     p26y = pontos[26][2] - pontos[24][2]
#     p1pdax = p24x
#     p1pday = p26y

#     if p1pda != 0:
#         angles[0] = (math.atan(p26y / p1bdbx) * 180)+360

#     print(angles)


#  # Angulo PDB =

#     p28x = 0
#     p26y = 0
#     p26x = pontos[26][1] - pontos[28][1]
#     p28y = pontos[28][2] - pontos[26][2]
#     p1pdbx = p26x
#     p1pdby = p28y

#     if p1pdb != 0:
#         angles[0] = (math.atan(p28x / p1bdby) * 180) + 360

#     print(angles)


#   # Angulo PEA =

#     p25x = 0
#     p23y = 0
#     p23x = pontos[23][1] - pontos[25][1]
#     p25y = pontos[25][2] - pontos[23][2]
#     p1peax = p23x
#     p1peay = p25y

#     if p1pea != 0:
#         angles[0] = (math.atan(p25x / p1beay) * 180)+360

#     print(angles)


#   # Angulo PEB =

#     p27x = 0
#     p25y = 0
#     p25x = pontos[25][1] - pontos[27][1]
#     p27y = pontos[27][2] - pontos[25][2]
#     p1pebx = p25x
#     p1peby = p27y

#     if p1peb != 0:
#         angles[0] = (math.atan(p27x / p1beby) * 180)+360

#     print(angles)

#     return angles

# Configurar a porta serial
porta_serial = serial.Serial('COM7', 115200)  # Replace 'COM4' with the correct serial port of your Arduino


time.sleep(2)  # Wait for serial communication to stabilize

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
detector = PoseDetector()

skip_frame = 1  # Skip sending data every x frames
contador = skip_frame

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the image!

    img = detector.findPose(img, False)
    lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)

    #             # BDA BDB BEA  BEB  PDA  PDB  PEA  PEB
    #     angles = [0,  0,   0,   0,   0,   0,   0,   0]
    angles = [0, 1, 2, 3, 4, 5, 6, 7]

    if len(lmList) != 0:
        angles[0] = round(detector.findAngle(img, 24, 12, 14))
        angles[1] = round(detector.findAngle(img, 24, 14, 16))
        angles[2] = 180 - round(detector.findAngle(img, 13, 11, 23)) # espelha movimento
        angles[3] = round(detector.findAngle(img, 15, 13, 23))
        angles[4] = round(detector.findAngle(img, 13, 23, 25))
        angles[5] = round(detector.findAngle(img, 26, 24, 14))
        angles[6] = round(detector.findAngle(img, 27, 25, 15)) 
        angles[7] = round(detector.findAngle(img, 28, 26, 16))

    if contador == 0:
        contador = skip_frame

        enviar_dados = ""
        for i in range(len(angles)):
            enviar_dados = enviar_dados + str(angles[i]) + ","
        enviar_dados = enviar_dados + "#"
        print(enviar_dados)

        porta_serial.write(enviar_dados.encode())

    contador = contador - 1

    cv2.imshow("Image", img)
    cv2.waitKey(1)

# Fechar a porta serial
porta_serial.close()
