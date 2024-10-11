import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = False

# Use DirectShow backend by adding the API preference cv2.CAP_DSHOW
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cam.isOpened():
    print("Error: Camera not opened.")
    exit()

# Initialize Face Mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
if face_mesh is None:
    print("Error: Face mesh initialization failed.")
    exit()

# Get screen size
screen_w, screen_h = pyautogui.size()

prev_eye_x, prev_eye_y = 0, 0
sensitivity = 35
prev_eyebrow_y = 0.038

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to read frame from camera.")
        break

    frame = cv2.flip(frame, 1)

    # Check if frame is empty
    if frame is None or frame.size == 0:
        print("Error: Captured frame is empty.")
        break

    # Convert frame to RGB
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except cv2.error as e:
        print(f"Error converting frame to RGB: {e}")
        break

    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark

        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            if id == 1:
                dist_x = x - prev_eye_x
                dist_y = y - prev_eye_y

                prev_eye_x, prev_eye_y = x, y

                move_x = dist_x * sensitivity
                move_y = dist_y * sensitivity

                screen_x = max(0, min(pyautogui.position().x + move_x, screen_w))
                screen_y = max(0, min(pyautogui.position().y + move_y, screen_h))

                try:
                    pyautogui.moveTo(screen_x, screen_y)
                except pyautogui.FailSafeException:
                    print("PyAutoGUI fail-safe triggered. Moving mouse to corner.")

        left_eye_upper = landmarks[145]
        left_eye_lower = landmarks[159]
        distance = abs(left_eye_upper.y - left_eye_lower.y)

        for landmark in [left_eye_upper, left_eye_lower]:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        if distance < 0.005:
            print("Click")
            pyautogui.click()
            pyautogui.sleep(1)

        right_eyebrow_upper = landmarks[70]
        right_eyebrow_lower = landmarks[103]
        left_eyebrow_upper = landmarks[300]
        left_eyebrow_lower = landmarks[333]

        for landmark in [right_eyebrow_upper, right_eyebrow_lower, left_eyebrow_upper, left_eyebrow_lower]:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)

        right_eyebrow_distance = right_eyebrow_upper.y - right_eyebrow_lower.y
        left_eyebrow_distance = left_eyebrow_upper.y - left_eyebrow_lower.y

        eyebrow_distance = round(((right_eyebrow_distance + left_eyebrow_distance) / 2), 4)
        print(eyebrow_distance)
        if eyebrow_distance < prev_eyebrow_y:
            print("Scroll up")
            pyautogui.scroll(150)
            pyautogui.sleep(1)
            prev_eyebrow_y = 0.038

    cv2.imshow('Eye Controlled Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
