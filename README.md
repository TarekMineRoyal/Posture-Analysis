# Biomechanical Ergonomic Evaluator

A real-time posture analysis system that connects to an edge camera stream to evaluate your spinal alignment. It utilizes a 3D Human Mesh Recovery engine to track internal S-Curve angles and dynamically alerts you when your posture deteriorates. 

## Key Features

* **3D Mesh Tracking**: Utilizes the ROMP (Robust One-stage Method for Person) library to calculate 3D joint rotations from standard video frames. 
* **Biomechanical Analysis**: Calculates precise 3D angles to track Lumbar Slump, Thoracic Hunch, and "Text Neck".
* **Dynamic Calibration**: Asks the user to sit in a healthy pose upon startup, taking 20 samples to establish a personalized baseline average.
* **Rolling Posture History**: Maintains a sliding window of the last 15 frames to evaluate posture consistency and eliminate false positives.
* **Asynchronous Audio Alarms**: Triggers an `alarm.wav` background sound via Windows `winsound` if 8 out of the last 15 frames show a significant deviation from your calibrated baseline.
* **Heads-Up UI Display**: Overlays real-time system FPS, neck/mid-spine/lower-spine angles in degrees, and color-coded status alerts ("HEALTHY S-CURVE" vs "FIX YOUR POSTURE!") directly onto the video feed using OpenCV.

## Project Structure

* `main.py`: The application entry point that handles the video capture loop, coordinates the evaluation steps, tracks the rolling 15-frame window, and triggers the audio alerts.
* `core/config.py`: Contains system constants such as the `STREAM_URL` and base geometric thresholds for the SMPL model.
* `core/calibration.py`: Collects initial pose samples to build a custom baseline array, enabling the system to track relative deviations (`deltas`) instead of static numbers.
* `core/math_utils.py`: Uses vector mathematics on specific SMPL mesh joints (pelvis, lumbar, thorax, upper_thorax, and neck) to compute the angle of curvature in a 3D space.
* `vision/pose_engine.py`: Encapsulates the ROMP neural network, which is configured specifically for real-time inference by turning off built-in rendering and focusing only on the primary person.
* `vision/ui_renderer.py`: Houses the OpenCV drawing functions to render the semi-transparent background panel and live metrics.

## System Requirements

* **Operating System:** Windows (The system relies on the `winsound` module for asynchronous alarm playback).
* **Hardware:** An NVIDIA GPU is heavily recommended (Tested on RTX 3050) for real-time ROMP mesh extraction.
* **Dependencies:** `opencv-python`, `romp`, `numpy`.
