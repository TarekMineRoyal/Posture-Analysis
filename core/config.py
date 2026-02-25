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
GOOD_NECK_THRESHOLD = 140  # Must be greater than this (closer to 180 is straight)
GOOD_TORSO_THRESHOLD = 15   # Must be less than this (closer to 0 is vertical)