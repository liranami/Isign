from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import cv2
import mediapipe as mp

mp_holistic = mp.solutions.holistic   # MediaPipe Holistic model
mp_show = mp.solutions.drawing_utils  # Drawing utilities

#ACTIONS = np.array(['לא','איפה','שלום','אתה','מה','שמח','עומד','השעה'])
ACTIONS = np.array(['אתה', 'מה', 'שמח', 'עומד', 'השעה', 'אני', 'איפה', 'השם', 'לא', 'עצוב', 'שלום', 'שלך'])

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Color Convert from BGR(cv2) to RBG
    image.flags.writeable = False                   # Image is not longer writeable
    results = model.process(image)                  # Make prediction
    image.flags.writeable = True                    # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Color Convert from RBG to BGR(cv2)
    return image, results


# Draw face, pose and hands connections
def show_landmarks(image, results):
    #mp_show.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
    #                       mp_show.DrawingSpec(color=(80,80,80), thickness=1, circle_radius=1))
    #mp_show.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
    #                       mp_show.DrawingSpec(color=(80,80,80), thickness=1, circle_radius=1))
    mp_show.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                           mp_show.DrawingSpec(color=(180,100,100), thickness=2, circle_radius=2))
    mp_show.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                           mp_show.DrawingSpec(color=(180,100,100), thickness=2, circle_radius=2))


def extract_keypoints(results):
    #pose = np.array([[res.x, res.y, res.z] for res in results.pose_landmarks.landmark]).flatten()\
    #    if results.pose_landmarks else np.zeros(33*4)
    left_hand = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()\
        if results.left_hand_landmarks else np.zeros(21*3)
    right_hand = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()\
        if results.right_hand_landmarks else np.zeros(21*3)
    #face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten()\
    #    if results.face_landmarks else np.zeros(468*3)
    return np.concatenate([ left_hand, right_hand])  # (1662,)pose, face,

model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(30, 126)))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dense(64))
#model.add(Dropout(0.2))
model.add(Dense(32))
model.add(Dense(ACTIONS.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.load_weights('model\\test_israeli_sing_language_model.h5')


sequence = []
sentence = []
predictions = []
threshold = 0.9
capture = cv2.VideoCapture(0)
# Set MediaPipe model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic_model:
    while capture.isOpened():
        ret, frame = capture.read()                                  # Read frame from webcam
        frame, results = mediapipe_detection(frame, holistic_model)  # Make detections
        #show_landmarks(frame, results)                               # Draw the landmarks
        keypoints = extract_keypoints(results)                       # wxtract key point from image(camera)
        sequence.append(keypoints)
        sequence = sequence[-30:]
        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            print(ACTIONS[np.argmax(res)], np.round(res, decimals=2))
            predictions.append(np.argmax(res))
            if np.unique(predictions[-15:])[0] == np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if ACTIONS[np.argmax(res)] != sentence[-1] and ACTIONS[np.argmax(res)]!='עומד':
                            sentence.append(ACTIONS[np.argmax(res)])
                            sequence = sequence[-20:]
                            print(sentence)
                            if len(sentence) > 12:
                                sentence = []
                    else:
                        sentence.append(ACTIONS[np.argmax(res)])
                        print(sentence)


        # print it to screen
        # ' '.join(sentence)


        cv2.imshow('camera', frame)                                  # Show to screen the frame
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()
