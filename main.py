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

        current_time = time.time()
        fps = 1 / (current_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = current_time
        timestamp_ms = int((current_time - start_time) * 1000)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # 1. Detect Poses
        pose_result = engine.process_frame(mp_image, timestamp_ms)

        # 2. Process and Render Results
        if pose_result.pose_landmarks and pose_result.pose_world_landmarks:
            draw_landmarks = pose_result.pose_landmarks[0]
            world_landmarks = pose_result.pose_world_landmarks[0]

            # --- DYNAMIC SIDE SELECTION ---
            if draw_landmarks[11].visibility > draw_landmarks[12].visibility:
                indices = (7, 11, 23)
                active_side = "LEFT"
            else:
                indices = (8, 12, 24)
                active_side = "RIGHT"

            ear_idx, shoulder_idx, hip_idx = indices

            ui_renderer.draw_skeleton(frame, draw_landmarks, indices)

            # Extract 3D points
            ear_3d = (world_landmarks[ear_idx].x, world_landmarks[ear_idx].y, world_landmarks[ear_idx].z)
            shoulder_3d = (
            world_landmarks[shoulder_idx].x, world_landmarks[shoulder_idx].y, world_landmarks[shoulder_idx].z)
            hip_3d = (world_landmarks[hip_idx].x, world_landmarks[hip_idx].y, world_landmarks[hip_idx].z)

            # Create a virtual vertical point 1 meter above the hip
            # (MediaPipe Y is positive downward, so subtract to go up)
            vertical_ref_3d = (hip_3d[0], hip_3d[1] - 1.0, hip_3d[2])

            # --- DUAL-METRIC CALCULATION ---
            # Neck Angle (Angle at shoulder between Ear and Hip)
            neck_angle = math_utils.calculate_angle_3d(ear_3d, shoulder_3d, hip_3d)

            # Torso Lean (Angle at Hip between Shoulder and Vertical Reference)
            torso_angle = math_utils.calculate_angle_3d(shoulder_3d, hip_3d, vertical_ref_3d)

            ui_renderer.draw_status(frame, neck_angle, torso_angle, fps, pose_detected=True, active_side=active_side)
        else:
            ui_renderer.draw_status(frame, 0, 0, fps, pose_detected=False)

        cv2.imshow('Distributed Ergonomic Evaluator - Live Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    engine.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()