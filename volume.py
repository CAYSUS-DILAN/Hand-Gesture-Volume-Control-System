import cv2
import mediapipe as mp
import pyautogui
import math

x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)  # Function to capture the video
my_hands = mp.solutions.hands.Hands()  # To capture our hands
drawing_utils = mp.solutions.drawing_utils  # To draw points in our hands

while True:
    _, image = webcam.read()  # Read the video frame
    image = cv2.flip(image, 1)  # Flip the image horizontally
    frame_height, frame_width, _ = image.shape      # Get frame dimensions
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB
    output = my_hands.process(rgb_image)  # Process the image for hand landmarks
    hands = output.multi_hand_landmarks  # Get the detected hands

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)  # Draw hand landmarks
            landmarks = hand.landmark  # Collect finger landmarks
            for id, landmark in enumerate(landmarks):  # Iterate through landmarks
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # Tip of the index finger
                    cv2.circle(image, (x, y), 8, (0, 255, 255), 3)
                    x1, y1 = x, y
                if id == 4:  # Tip of the thumb
                    cv2.circle(image, (x, y), 8, (0, 0, 255), 3)
                    x2, y2 = x, y

        # Calculate Euclidean distance between thumb and index finger
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Draw a line between thumb and index finger
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

        # Volume control based on distance
        if dist > 50:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")

    cv2.imshow("Hand volume control using python", image)

    key = cv2.waitKey(10)  # Wait for 10 ms
    if key == 27:  # ESC key to exit
        break

webcam.release()  # Release webcam
cv2.destroyAllWindows()  # Destroy all windows
