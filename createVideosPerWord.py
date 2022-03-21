import cv2
import numpy as np
import os
import time
import mediapipe as mp
from matplotlib import pyplot as plt

ACTIONS = np.array(['שלום', 'תודה'])
mp_holistic = mp.solutions.holistic   # MediaPipe Holistic model
mp_show = mp.solutions.drawing_utils  # Drawing utilities


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Color Convert from BGR(cv2) to RBG
    image.flags.writeable = False                   # Image is not longer writeable
    results = model.process(image)                  # Make prediction
    image.flags.writeable = True                    # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Color Convert from RBG to BGR(cv2)
    return image, results


def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten()\
        if results.pose_landmarks else np.zeros(33*4)
    left_hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()\
        if results.left_hand_landmarks else np.zeros(21*3)
    right_hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()\
        if results.right_hand_landmarks else np.zeros(21*3)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten()\
        if results.face_landmarks else np.zeros(468*3)
    return np.concatenate([pose, face, left_hand, right_hand])  # (1662,)


DATA_PATH = os.path.join('Sign_Language_Data')
sing_language_actions = ACTIONS  # Actions is the words we will translate
numbers_of_videos = 30  # Number of videos to each word
video_length = 30       # Frames we take to analyze

# Create 30 videos of each word,
# Each word will have folder and inside 30 different videos (with 30 frame - 1662 DATA each)
for sing in sing_language_actions:
    for video in range(numbers_of_videos):
        try:
            os.makedirs(os.path.join(DATA_PATH, sing, str(video)))
        except:
            pass



#cap = cv2.VideoCapture('chaplin.mp4')

# Check if camera opened successfully
#if (cap.isOpened() == False):
#    print("Error opening video stream or file")

capture = cv2.VideoCapture(0)
# Set MediaPipe model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic_model:
    for sing in sing_language_actions:
        for video in range(numbers_of_videos):
            for frame_number in range(video_length):

                ret, frame = capture.read()                                  # Read frame from webcam
                frame, results = mediapipe_detection(frame, holistic_model)  # Make detections

                cv2.putText(frame, 'Collecting for {} video number {}'.format(sing, video), (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                if frame_number == 0:
                    cv2.putText(frame, 'STARTING TO COLLECT', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4, cv2.LINE_AA)
                    cv2.waitKey(1200)

                keypoints = extract_keypoints(results)
                np_path = os.path.join(DATA_PATH, sing, str(video), str(frame_number))
                np.save(np_path, keypoints)
                cv2.imshow('camera', frame)                                  # Show to screen the frame
                if cv2.waitKey(10) == ord('q'):
                    break
    capture.release()
    cv2.destroyAllWindows()