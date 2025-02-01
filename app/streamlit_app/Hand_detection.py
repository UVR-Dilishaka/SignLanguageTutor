import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def normalized_landmarks(landmarks):
    """Normalize and flatten landmarks for processing."""
    # Assumes landmarks is an (21,3) np array
    normalized_landmarks = landmarks - landmarks[0]
    return normalized_landmarks

def calculate_angle_bulk(landmarks, point_indices):
    p1 = landmarks[[i[0] for i in point_indices]]
    p2 = landmarks[[i[1] for i in point_indices]]
    p3 = landmarks[[i[2] for i in point_indices]]

    # Compute vectors
    ba = p1 - p2  # Vector from p2 to p1
    bc = p3 - p2  # Vector from p2 to p3

    # Compute dot products and magnitudes
    dot_products = np.sum(ba * bc, axis=1)  # Dot product for each triplet
    magnitudes_ba = np.linalg.norm(ba, axis=1)
    magnitudes_bc = np.linalg.norm(bc, axis=1)

    # Calculate angles (clip to handle floating-point errors)
    cosine_angles = dot_products / (magnitudes_ba * magnitudes_bc)
    cosine_angles = np.clip(cosine_angles, -1.0, 1.0)
    angles_rad = np.arccos(cosine_angles)

    # Convert to degrees
    angles_deg = np.rad2deg(angles_rad)
    return angles_deg


def angle_listing(landmarks):
    # Define the triplets of points for which angles are needed
    point_indices = [
        (1, 2, 3), (0, 5, 6), (0, 9, 10), (0, 13, 14), (0, 17, 18),
        (5, 6, 7), (9, 10, 11), (13, 14, 15), (17, 18, 19),
        (6, 7, 8), (10, 11, 12), (14, 15, 16), (18, 19, 20),
        (0, 1, 2), (2, 3, 4), (2, 1, 5)
    ]

    # Calculate angles in bulk
    angle_list = calculate_angle_bulk(landmarks, point_indices)
    return angle_list


def capture_hand_landmarks():
    # Initialize the webcam capture
    cap = cv2.VideoCapture(0)  # 0 for default webcam

    # Set up Mediapipe Hands with desired settings
    with mp_hands.Hands(
        static_image_mode=False,  # Real-time mode
        max_num_hands=1,         # Detect one hand at a time
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Flip the frame horizontally for a mirror-like effect
            frame = cv2.flip(frame, 1)

            # Convert the frame to RGB (Mediapipe uses RGB images)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with Mediapipe Hands
            results = hands.process(rgb_frame)

            # Prepare an empty landmarks array
            landmarks_array = np.zeros((21, 3))

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Extract landmarks as a NumPy array
                    landmarks_array = np.array([
                        [lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark
                    ])

                    # Draw the hand landmarks on the frame
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

            # Display the frame with landmarks
            cv2.imshow("Hand Landmarks", frame)

            # Yield the landmarks array for each frame
            yield landmarks_array

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()


# Prints landmarks, normalized landmarks, and angles for each frame
for landmarks in capture_hand_landmarks():
    #print(f"Landmarks for current frame: {landmarks}")
    # print(f"Norm_Landmarks for current frame:\n {normalized_landmarks(landmarks)}")
    print(f"Angles for current frame: {angle_listing(landmarks)}")
    print("-" * 50)  # Add a separator for clarity




