"""
Chapter 3: Inverse Kinematics

This example demonstrates:
1. Forward kinematics: joint angles -> end-effector position
2. Inverse kinematics: desired position -> joint angles
3. Using PyBullet's built-in IK solver
4. Implementing a simple 2-link arm IK analytically

Inverse kinematics is fundamental to robot arm control.
"""

import pybullet as p
import pybullet_data
import math
import time
from typing import List, Tuple, Optional


def analytical_2link_ik(
    target_x: float,
    target_y: float,
    L1: float = 1.0,
    L2: float = 1.0
) -> Optional[Tuple[float, float]]:
    """
    Analytical inverse kinematics for a 2-link planar arm.

    This is the "textbook" solution for a 2-DOF planar arm.

    Args:
        target_x: Target X position
        target_y: Target Y position
        L1: Length of first link
        L2: Length of second link

    Returns:
        (theta1, theta2) joint angles in radians, or None if unreachable
    """
    # Distance to target
    d = math.sqrt(target_x**2 + target_y**2)

    # Check if target is reachable
    if d > L1 + L2:
        return None  # Too far
    if d < abs(L1 - L2):
        return None  # Too close

    # Law of cosines to find elbow angle
    cos_theta2 = (d**2 - L1**2 - L2**2) / (2 * L1 * L2)

    # Clamp to valid range (numerical precision)
    cos_theta2 = max(-1, min(1, cos_theta2))

    # Elbow angle (we choose elbow-down configuration)
    theta2 = math.acos(cos_theta2)

    # Shoulder angle
    beta = math.atan2(target_y, target_x)
    alpha = math.atan2(L2 * math.sin(theta2), L1 + L2 * math.cos(theta2))
    theta1 = beta - alpha

    return (theta1, theta2)


def forward_kinematics_2link(
    theta1: float,
    theta2: float,
    L1: float = 1.0,
    L2: float = 1.0
) -> Tuple[float, float]:
    """
    Forward kinematics for a 2-link planar arm.

    Args:
        theta1: First joint angle (radians)
        theta2: Second joint angle (radians)
        L1: Length of first link
        L2: Length of second link

    Returns:
        (x, y) position of end effector
    """
    # Elbow position
    elbow_x = L1 * math.cos(theta1)
    elbow_y = L1 * math.sin(theta1)

    # End effector position
    end_x = elbow_x + L2 * math.cos(theta1 + theta2)
    end_y = elbow_y + L2 * math.sin(theta1 + theta2)

    return (end_x, end_y)


def run_ik_demo_pybullet(use_gui: bool = True) -> dict:
    """
    Demonstrate inverse kinematics using PyBullet's Kuka robot arm.

    Args:
        use_gui: If True, opens a visualization window

    Returns:
        dict with IK solution results
    """
    # Setup
    physics_client = p.connect(p.GUI if use_gui else p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)

    # Load environment and robot
    plane_id = p.loadURDF("plane.urdf")
    robot_id = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)

    # Get number of joints
    num_joints = p.getNumJoints(robot_id)

    # End effector link index (typically the last link)
    end_effector_link = num_joints - 1

    # Target position for end effector
    target_position = [0.5, 0.3, 0.5]

    # Solve IK
    joint_positions = p.calculateInverseKinematics(
        robot_id,
        end_effector_link,
        target_position
    )

    # Apply the solution
    for i, pos in enumerate(joint_positions):
        if i < num_joints:
            p.setJointMotorControl2(
                robot_id,
                i,
                p.POSITION_CONTROL,
                targetPosition=pos,
                force=500
            )

    # Simulate to let robot reach target
    for _ in range(240 * 2):  # 2 seconds
        p.stepSimulation()
        if use_gui:
            time.sleep(1.0 / 240.0)

    # Get actual end effector position
    link_state = p.getLinkState(robot_id, end_effector_link)
    actual_position = link_state[0]

    # Calculate error
    error = math.sqrt(sum((a - t)**2 for a, t in zip(actual_position, target_position)))

    p.disconnect()

    return {
        "target_position": target_position,
        "actual_position": actual_position,
        "position_error": error,
        "joint_solution": joint_positions
    }


def test_analytical_ik():
    """Test the analytical 2-link IK solution."""
    print("Analytical 2-Link IK Test")
    print("=" * 40)

    # Test cases
    test_cases = [
        (1.5, 0.5),   # Reachable
        (0.5, 1.5),   # Reachable
        (1.0, 1.0),   # Reachable
        (3.0, 0.0),   # Unreachable (too far)
        (0.0, 0.0),   # Unreachable (at origin)
    ]

    for target_x, target_y in test_cases:
        result = analytical_2link_ik(target_x, target_y)

        print(f"\nTarget: ({target_x:.1f}, {target_y:.1f})")

        if result is None:
            print("  Result: UNREACHABLE")
        else:
            theta1, theta2 = result
            # Verify with forward kinematics
            actual_x, actual_y = forward_kinematics_2link(theta1, theta2)

            print(f"  Theta1: {math.degrees(theta1):.1f} deg")
            print(f"  Theta2: {math.degrees(theta2):.1f} deg")
            print(f"  FK check: ({actual_x:.3f}, {actual_y:.3f})")

            error = math.sqrt((actual_x - target_x)**2 + (actual_y - target_y)**2)
            print(f"  Error: {error:.6f}")


if __name__ == "__main__":
    # Test analytical solution first
    test_analytical_ik()

    print("\n" + "=" * 40)
    print("PyBullet IK Demo (Kuka Robot Arm)")
    print("=" * 40)

    result = run_ik_demo_pybullet(use_gui=True)

    print(f"\nTarget position:  {result['target_position']}")
    print(f"Actual position:  [{result['actual_position'][0]:.3f}, "
          f"{result['actual_position'][1]:.3f}, {result['actual_position'][2]:.3f}]")
    print(f"Position error:   {result['position_error']:.4f} meters")
