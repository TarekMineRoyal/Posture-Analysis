import numpy as np


class CalibrationManager:
    def __init__(self, target_samples=15):
        self.target_samples = target_samples
        self.samples = []
        self.baseline = None  # Will store (neck, mid, low)
        self.is_calibrated = False

    def collect_sample(self, neck, mid, low):
        """Adds a sample during the calibration phase."""
        self.samples.append([neck, mid, low])
        progress = len(self.samples) / self.target_samples

        if len(self.samples) >= self.target_samples:
            # Calculate the average of all collected samples
            self.baseline = np.mean(self.samples, axis=0)
            self.is_calibrated = True
            return 1.0
        return progress

    def get_deltas(self, neck, mid, low):
        """Calculates how much the current pose differs from the baseline."""
        if not self.is_calibrated:
            return 0, 0, 0

        # We use absolute difference to see 'change' in any direction
        d_neck = neck - self.baseline[0]
        d_mid = mid - self.baseline[1]
        d_low = low - self.baseline[2]
        return d_neck, d_mid, d_low