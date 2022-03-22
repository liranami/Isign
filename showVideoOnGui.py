import tkinter
import PIL
import cv2
import numpy as np
import os
import time
import mediapipe as mp
from threading import Thread, Lock
import userGUI
mp_holistic = mp.solutions.holistic  # MediaPipe Holistic model
mp_show = mp.solutions.drawing_utils  # Drawing utilities


stop = False


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Color Convert from BGR(cv2) to RBG
    image.flags.writeable = False  # Image is not longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Color Convert from RBG to BGR(cv2)
    return image, results


# Draw face, pose and hands connections
def show_landmarks(image, results):
    mp_show.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                            mp_show.DrawingSpec(color=(80, 80, 80), thickness=1, circle_radius=1))
    mp_show.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                            mp_show.DrawingSpec(color=(80, 80, 80), thickness=1, circle_radius=1))
    mp_show.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                            mp_show.DrawingSpec(color=(180, 100, 100), thickness=2, circle_radius=2))
    mp_show.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                            mp_show.DrawingSpec(color=(180, 100, 100), thickness=2, circle_radius=2))


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten() \
        if results.pose_landmarks else np.zeros(33 * 4)
    left_hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() \
        if results.left_hand_landmarks else np.zeros(21 * 3)
    right_hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() \
        if results.right_hand_landmarks else np.zeros(21 * 3)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() \
        if results.face_landmarks else np.zeros(468 * 3)
    return np.concatenate([pose, face, left_hand, right_hand])  # (1662,)


def stopShowVideo(tf):
    global stop
    stop = tf


def showVideo(cameraNum, window):
    global stop
    capture = cv2.VideoCapture(int(cameraNum) - 1)
    canvas = tkinter.Canvas(window, width=512, height=410)
    canvas.place(x=28, y=107)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic_model:
        while stop:
            ret, frame = capture.read()  # Read frame from webcam
            frame, results = mediapipe_detection(frame, holistic_model)  # Make detections
            show_landmarks(frame, results)
            #photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            #canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
            #self.canvas.image = photo
            # keypoints = extract_keypoints(results)
            cv2.imshow('camera', frame)  # Show to screen the frame
            if cv2.waitKey(10) == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
