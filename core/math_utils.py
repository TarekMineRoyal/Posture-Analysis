"""Mathematical utilities for vector and angle calculations."""
import math


def calculate_angle(a, b, c):
    """
    Calculates the 2D angle at point 'b' given points a, b, and c.
    Returns the angle in degrees.
    """
    # Create vectors BA and BC
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    # Dot product and magnitudes
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    mag_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    # Prevent division by zero if points overlap
    if mag_ba * mag_bc == 0:
        return 0

    # Calculate angle in radians and convert to degrees
    cos_angle = dot_product / (mag_ba * mag_bc)

    # Clamp the value between -1.0 and 1.0 to prevent floating point domain errors
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.degrees(math.acos(cos_angle))