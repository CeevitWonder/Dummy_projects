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
