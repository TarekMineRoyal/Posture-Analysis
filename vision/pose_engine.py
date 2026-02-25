"""Handles the MediaPipe Pose Landmarker initialization and processing."""
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
from core import config


class PoseEngine:
    def __init__(self):
        self._ensure_model_exists()

        options = vision.PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=config.MODEL_PATH),
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=config.MIN_POSE_DETECTION_CONFIDENCE,
            min_pose_presence_confidence=config.MIN_POSE_PRESENCE_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        # Create the landmarker instance
        self.landmarker = vision.PoseLandmarker.create_from_options(options)

    def _ensure_model_exists(self):
        """Downloads the MediaPipe model if it doesn't exist locally."""
        if not os.path.exists(config.MODEL_PATH):
            print(f"Downloading Heavy MediaPipe model to {config.MODEL_PATH}...")
            urllib.request.urlretrieve(config.MODEL_URL, config.MODEL_PATH)
            print("Download complete.")

    def process_frame(self, mp_image, timestamp_ms):
        """Processes an image frame and returns the pose landmarks."""
        return self.landmarker.detect_for_video(mp_image, timestamp_ms)

    def close(self):
        """Cleans up the MediaPipe resources."""
        self.landmarker.close()