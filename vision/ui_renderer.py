"""Handles OpenCV drawing and UI overlays."""
import cv2
from core import config

def draw_skeleton(frame, landmarks, indices):
    """Draws nodes and connections for the dynamically selected side."""
    h, w, _ = frame.shape
    ear_idx, shoulder_idx, hip_idx = indices

    ear = (int(landmarks[ear_idx].x * w), int(landmarks[ear_idx].y * h))
    shoulder = (int(landmarks[shoulder_idx].x * w), int(landmarks[shoulder_idx].y * h))
    hip = (int(landmarks[hip_idx].x * w), int(landmarks[hip_idx].y * h))

    # Draw pure vertical reference line from hip (for visual reference only)
    vertical_ref = (hip[0], hip[1] - 150) # Just extending 150 pixels up
    cv2.line(frame, hip, vertical_ref, (255, 255, 255), 2, lineType=cv2.LINE_AA)

    # Draw nodes
    cv2.circle(frame, ear, 8, (0, 255, 0), -1)
    cv2.circle(frame, shoulder, 8, (0, 255, 0), -1)
    cv2.circle(frame, hip, 8, (0, 255, 0), -1)

    # Draw vectors
    cv2.line(frame, ear, shoulder, (255, 255, 0), 3)
    cv2.line(frame, shoulder, hip, (255, 255, 0), 3)

def draw_status(frame, neck_angle, torso_angle, fps, pose_detected=True, active_side="NONE"):
    """Overlays the angles, ergonomic status, active side, and FPS."""
    cv2.putText(frame, f"FPS: {int(fps)} | Side: {active_side}", (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    if pose_detected:
        # Evaluate Neck
        neck_good = neck_angle > config.GOOD_NECK_THRESHOLD
        neck_color = (0, 255, 0) if neck_good else (0, 0, 255)
        neck_status = "OK" if neck_good else "TEXT NECK"

        # Evaluate Torso
        torso_good = torso_angle < config.GOOD_TORSO_THRESHOLD
        torso_color = (0, 255, 0) if torso_good else (0, 0, 255)
        torso_status = "OK" if torso_good else "LEANING"

        # Overall Status
        if neck_good and torso_good:
            overall_status = "PERFECT POSTURE"
            overall_color = (0, 255, 0)
        else:
            overall_status = "SLOUCHING"
            overall_color = (0, 0, 255)

        # Draw UI Block
        cv2.putText(frame, f"Neck: {int(neck_angle)} deg [{neck_status}]", (15, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, neck_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"Torso: {int(torso_angle)} deg [{torso_status}]", (15, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, torso_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"Status: {overall_status}", (15, 175),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, overall_color, 3, cv2.LINE_AA)
    else:
        cv2.putText(frame, "Status: NO POSE DETECTED", (15, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2, cv2.LINE_AA)