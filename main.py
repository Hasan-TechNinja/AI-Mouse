import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)  # Open the default camera
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
# screen_width, screen_height = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get()
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    _, frame = cap.read()  # Read a frame from the camera
    frame = cv2.flip(frame, 1)  # Flip it horizontally
    frame_height, frame_width, _ = frame.shape  # Get the frame dimensions
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    output = hand_detector.process(rgb_frame)  # Process with Mediapipe
    hands = output.multi_hand_landmarks  # Get detected hand landmarks

    if hands:  # If hands are detected
        for hand in hands:  # Iterate over the detected hands
            drawing_utils.draw_landmarks(frame, hand)  # Draw landmarks on the frame
            # Corrected: access `hand.landmark` instead of `hands.landmark`
            for id, landmark in enumerate(hand.landmark):
                # Transform normalized coordinates into pixel coordinates
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                print(x, y)  # Print the pixel coordinates
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                    pyautogui.moveTo(index_x, index_y)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print("Outside", abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)

    cv2.imshow('Virtual Mouse', frame)  # Display the frame

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
