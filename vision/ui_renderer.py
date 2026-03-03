"""Handles OpenCV drawing and UI overlays for Biomechanical data."""
import cv2

def draw_status(frame, neck, mid, low, fps, pose_detected=True, is_bad=False, alarm_active=False):
    """Overlays the biomechanical spinal curvature data onto the frame."""

    # Draw a dark, semi-transparent background panel
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (480, 250), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Base FPS Display
    cv2.putText(frame, f"System FPS: {int(fps)}", (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    if pose_detected:
        status_color = (0, 0, 255) if is_bad else (0, 255, 0)

        # Override the status text if the alarm is actively ringing
        if alarm_active:
            status_text = "FIX YOUR POSTURE!"
            status_color = (0, 165, 255) # Orange/Warning color
        else:
            status_text = "SPINAL MISALIGNMENT" if is_bad else "HEALTHY S-CURVE"

        # Draw the Data Metrics
        cv2.putText(frame, f"Neck Angle:  {neck:>5.1f} deg", (15, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"Mid Spine:   {mid:>5.1f} deg", (15, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"Lower Spine: {low:>5.1f} deg", (15, 165),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2, cv2.LINE_AA)

        # Overall System Status
        cv2.putText(frame, f"STATUS: {status_text}", (15, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "STATUS: NO SUBJECT DETECTED", (15, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2, cv2.LINE_AA)