"""Biomechanical mathematical utilities using 3D Mesh Joints."""
import math

# ROMP 3D Joint Indices
SMPL_JOINTS = {
    'pelvis': 0,
    'lumbar': 3,
    'thorax': 6,
    'upper_thorax': 9,
    'neck': 12
}

def calculate_angle_3d(a, b, c):
    """Calculates the 3D angle at point 'b' given 3D points a, b, and c."""
    ba = (a[0] - b[0], a[1] - b[1], a[2] - b[2])
    bc = (c[0] - b[0], c[1] - b[1], c[2] - b[2])

    dot_product = ba[0]*bc[0] + ba[1]*bc[1] + ba[2]*bc[2]
    mag_ba = math.sqrt(ba[0]**2 + ba[1]**2 + ba[2]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2 + bc[2]**2)

    if mag_ba * mag_bc == 0:
        return 0

    cos_angle = dot_product / (mag_ba * mag_bc)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    return math.degrees(math.acos(cos_angle))

def evaluate_spine(smpl_joints):
    """
    Takes the 3D spatial joints from the mesh and calculates internal S-Curve angles.
    """
    # Grab the first person's 3D joints
    joints = smpl_joints[0]

    pelvis = joints[SMPL_JOINTS['pelvis']]
    lumbar = joints[SMPL_JOINTS['lumbar']]
    thorax = joints[SMPL_JOINTS['thorax']]
    upper_thorax = joints[SMPL_JOINTS['upper_thorax']]
    neck = joints[SMPL_JOINTS['neck']]

    # 1. Lumbar Slump (Angle at Lumbar between Pelvis and Thorax)
    lumbar_curve = calculate_angle_3d(thorax, lumbar, pelvis)

    # 2. Thoracic Hunch (Angle at Thorax between Lumbar and Upper Thorax)
    thoracic_curve = calculate_angle_3d(upper_thorax, thorax, lumbar)

    # 3. Text Neck (Angle at Upper Thorax between Thorax and Neck)
    neck_curve = calculate_angle_3d(neck, upper_thorax, thorax)

    return lumbar_curve, thoracic_curve, neck_curve