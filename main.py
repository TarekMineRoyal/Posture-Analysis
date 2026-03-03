import cv2
import time
import winsound
import threading
from collections import deque

from core import config, math_utils
from core.calibration import CalibrationManager
from vision.pose_engine import PoseEngine
from vision import ui_renderer


# Background function to play the beep without pausing the video feed
# We use a raw string (r"") so Windows backslashes don't break the path
ALARM_PATH = r"D:\DEV\Python\Posture_Evaluator\alarm.wav"

def play_alarm_sound():
    # SND_ASYNC: Play in background
    # SND_FILENAME: Treat the string as a file path
    # SND_NODEFAULT: Fail silently if the file is missing (don't play the Windows Ding)
    flags = winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT
    winsound.PlaySound(ALARM_PATH, flags)


def main():
    print(f"Connecting to Edge Sensor at: {config.STREAM_URL}...")
    cap = cv2.VideoCapture(config.STREAM_URL)
    engine = PoseEngine()
    calibrator = CalibrationManager(target_samples=20)

    prev_frame_time = 0
    last_beep_time = 0

    # --- ROLLING WINDOW SETUP ---
    # A queue that holds exactly 15 frames. Oldest frame drops off automatically.
    posture_history = deque(maxlen=15)

    print("SYSTEM START: Please sit in your HEALTHY pose for calibration...")

    while True:
        success, frame = cap.read()
        if not success: break

        current_time = time.time()
        fps = 1 / (current_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = current_time

        outputs = engine.process_frame(frame)
        is_bad = False
        alarm_active = False

        if outputs is not None and 'joints' in outputs:
            neck, mid, low = math_utils.evaluate_spine(outputs['joints'])

            if not calibrator.is_calibrated:
                progress = calibrator.collect_sample(neck, mid, low)
                cv2.rectangle(frame, (50, 400), (450, 430), (50, 50, 50), -1)
                cv2.rectangle(frame, (50, 400), (50 + int(400 * progress), 430), (0, 255, 255), -1)
                cv2.putText(frame, f"CALIBRATING... {int(progress * 100)}%", (60, 390),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                ui_renderer.draw_status(frame, neck, mid, low, fps, pose_detected=True)
            else:
                d_neck, d_mid, d_low = calibrator.get_deltas(neck, mid, low)

                # Check if this specific frame is bad
                is_bad = (abs(d_neck) > 4.0) or (abs(d_mid) > 4.0) or (abs(d_low) > 6.0)

                # Push the current frame's status into the rolling window
                posture_history.append(is_bad)

                # --- ALARM LOGIC ---
                # Count how many 'True' (bad) frames are in the last 15
                bad_frame_count = posture_history.count(True)

                if bad_frame_count >= 8:
                    alarm_active = True
                    # Only trigger the file once every 2 seconds
                    if current_time - last_beep_time > 2.0:
                        play_alarm_sound()  # No threading needed thanks to SND_ASYNC!
                        last_beep_time = current_time

                ui_renderer.draw_status(frame, neck, mid, low, fps,
                                        pose_detected=True,
                                        is_bad=is_bad,
                                        alarm_active=alarm_active)
        else:
            ui_renderer.draw_status(frame, 0, 0, 0, fps, pose_detected=False)

        cv2.imshow('Biomechanical Ergonomic Evaluator', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

        time.sleep(max(0, 0.2 - (time.time() - current_time)))

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()