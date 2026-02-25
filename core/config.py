"""Configuration settings and constants for the Ergonomic Evaluator."""

# --- Model Configurations ---
MODEL_PATH = 'pose_landmarker_heavy.task'
MODEL_URL = 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task'

# --- Camera/Stream Configurations ---
STREAM_URL = "http://10.255.23.185:8080/video"

# --- MediaPipe Configurations ---
MIN_POSE_DETECTION_CONFIDENCE = 0.6
MIN_POSE_PRESENCE_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# --- Ergonomic Thresholds ---
# Currently a static threshold; will be updated to dynamic in Phase 4
GOOD_POSTURE_THRESHOLD = 150