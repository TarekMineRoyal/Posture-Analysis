"""Main entry point for the Distributed Ergonomic Evaluator."""
import cv2
import time
import mediapipe as mp

from core import config, math_utils
from vision.pose_engine import PoseEngine
from vision import ui_renderer


def main():
    print(f"Connecting to Edge Sensor at: {config.STREAM_URL}...")
    cap = cv2.VideoCapture(config.STREAM_URL)

    # Initialize our custom MediaPipe wrapper
    engine = PoseEngine()

    prev_frame_time = 0
    start_time = time.time()

    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Failed to grab frame.")
            break

        # Calculate timing and FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = current_time
        timestamp_ms = int((current_time - start_time) * 1000)

        # Prepare image for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # 1. Detect Poses
        pose_result = engine.process_frame(mp_image, timestamp_ms)

        # 2. Process and Render Results
        if pose_result.pose_landmarks:
            landmarks = pose_result.pose_landmarks[0]

            # Draw skeleton and extract points
            ear, shoulder, hip = ui_renderer.draw_skeleton(frame, landmarks)

            # Calculate angle
            posture_angle = math_utils.calculate_angle(ear, shoulder, hip)

            # Draw UI
            ui_renderer.draw_status(frame, posture_angle, fps, pose_detected=True)
        else:
            ui_renderer.draw_status(frame, 0, fps, pose_detected=False)

        # 3. Display Output
        cv2.imshow('Distributed Ergonomic Evaluator - Live Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    engine.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()