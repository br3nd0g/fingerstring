import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

def detectFingers(image):

    tips = None

    results = hands.process(image)

    if results.multi_hand_landmarks:

        tips = []
            
        for hand_landmarks in results.multi_hand_landmarks:

            index_x = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x
            index_y = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y

            thumb_x = hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].x
            thumb_y = hand_landmarks.landmark[mpHands.HandLandmark.THUMB_TIP].y

            # draw hand points
            # mpDraw.draw_landmarks(image, hand_landmarks, mpHands.HAND_CONNECTIONS)

            tipsForHand = {
                "index": {"x": index_x, "y": index_y},
                "thumb": {"x": thumb_x, "y": thumb_y}
            }

            tips.append(tipsForHand)

    return tips