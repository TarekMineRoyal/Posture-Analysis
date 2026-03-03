"""Configuration settings and constants for the Ergonomic Evaluator."""

# --- Camera/Stream Configurations ---
STREAM_URL = "http://10.255.23.185:8080/video"

# --- SMPL Geometric Thresholds (Inner Spine Angles) ---
# A straight spine is ~180 degrees. Bending drops the angle.
MIN_NECK_ANGLE = 130.0
MIN_THORACIC_ANGLE = 140.0
MIN_LUMBAR_ANGLE = 110.0

# Tolerances (in percentages or degrees)
NECK_DROP_TOLERANCE = 10.0  # Alert if neck drops 10 degrees from baseline
THORACIC_BEND_TOLERANCE = 8.0