import cv2
import mediapipe as mp
import math

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
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get frame dimensions
            h, w, _ = frame.shape

            # Wrist (landmark 0) and middle MCP (landmark 9)
            wrist = hand_landmarks.landmark[0]  # Wrist
            middle_mcp = hand_landmarks.landmark[9]  # Middle MCP (fixed to landmark 9)

            # Convert normalized coordinates to pixel values
            wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
            middle_mcp_x, middle_mcp_y = int(middle_mcp.x * w), int(middle_mcp.y * h)

            # Calculate the distance between wrist and middle MCP
            distance = math.sqrt((middle_mcp_x - wrist_x) ** 2 + (middle_mcp_y - wrist_y) ** 2)

            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw a line from wrist to middle MCP
            cv2.line(frame, (wrist_x, wrist_y), (middle_mcp_x, middle_mcp_y), (0, 255, 0), 2)

            # Display the length of the line on the frame
            cv2.putText(frame, f"Length: {int(distance)} px", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Output message if the distance is less than 180px
            if distance < 120:
                print("Move the hand closer to the camera\n")

    # Display the video feed with landmarks and the line
    cv2.imshow('Hand Distance Detection', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
