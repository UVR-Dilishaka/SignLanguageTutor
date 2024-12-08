# Testing if the model can detect only one specified hand.
# If different signs has different hands predefine them

import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and process the frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Check if any hands are detected
    if result.multi_hand_landmarks and result.multi_handedness:
        # Loop through each detected hand and its handedness
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            # Check if the hand is the left hand
            label = handedness.classification[0].label  # 'Left' or 'Right'
            if label == "Left":
                # Print landmark coordinates for the left hand
                for i, landmark in enumerate(hand_landmarks.landmark):
                    print(f"Landmark {i}: x={landmark.x:.3f}, y={landmark.y:.3f}, z={landmark.z:.3f}")

                # Draw landmarks only for the left hand
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                break  # Exit loop after processing the first detected left hand

    # Display the video feed
    cv2.imshow('Left Hand Detection', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
