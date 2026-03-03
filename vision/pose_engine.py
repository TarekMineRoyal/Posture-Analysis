"""Handles the 3D Human Mesh Recovery using ROMP."""
import cv2
import romp

class PoseEngine:
    def __init__(self):
        print("Initializing ROMP 3D Mesh Engine on RTX 3050...")

        # 1. Load the default ROMP configuration
        self.settings = romp.main.default_settings

        # 2. Optimize for real-time inference
        self.settings.calc_smpl = True         # WE NEED THIS: Calculates joint rotations
        self.settings.render_mesh = False      # Disable built-in rendering to save VRAM/time
        self.settings.show_largest = True      # Only track the primary person (ignore people in background)

        # 3. Spin up the neural network
        self.model = romp.ROMP(self.settings)
        print("ROMP Engine loaded successfully.")

    def process_frame(self, bgr_frame):
        """
        Processes a standard OpenCV BGR frame.
        Returns a dictionary containing the SMPL mesh data, or None if no person is found.
        """
        outputs = self.model(bgr_frame)
        return outputs

    def close(self):
        """No strict cleanup required for ROMP, but keeps our API consistent."""
        pass