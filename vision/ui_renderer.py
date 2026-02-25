"""Handles OpenCV drawing and UI overlays."""
import cv2
from core import config


def draw_skeleton(frame, landmarks):
    """Draws nodes and connections for the left side of the body."""
    h, w, _ = frame.shape

    # Extract Left Side Indices (7, 11, 23)
    left_ear = (int(landmarks[7].x * w), int(landmarks[7].y * h))
    left_shoulder = (int(landmarks[11].x * w), int(landmarks[11].y * h))
    left_hip = (int(landmarks[23].x * w), int(landmarks[23].y * h))

    # Draw nodes
    cv2.circle(frame, left_ear, 8, (0, 255, 0), -1)
    cv2.circle(frame, left_shoulder, 8, (0, 255, 0), -1)
    cv2.circle(frame, left_hip, 8, (0, 255, 0), -1)

    # Draw vectors
    cv2.line(frame, left_ear, left_shoulder, (255, 255, 0), 3)
    cv2.line(frame, left_shoulder, left_hip, (255, 255, 0), 3)

    return left_ear, left_shoulder, left_hip


def draw_status(frame, angle, fps, pose_detected=True):
    """Overlays the angle, ergonomic status, and FPS onto the frame."""
    # Base FPS Display
    cv2.putText(frame, f"Sensor FPS: {int(fps)}", (15, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    if pose_detected:
        color = (0, 255, 0) if angle > config.GOOD_POSTURE_THRESHOLD else (0, 0, 255)
        status = "GOOD" if angle > config.GOOD_POSTURE_THRESHOLD else "SLOUCHING"

        cv2.putText(frame, f"Spine Angle: {int(angle)} deg", (15, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"Status: {status}", (15, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "Status: NO POSE DETECTED", (15, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2, cv2.LINE_AA)