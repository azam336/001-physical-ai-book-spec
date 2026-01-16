"""
Chapter 2: Sensor Basics

This example demonstrates how to:
1. Read joint position sensors (encoders)
2. Simulate a simple distance sensor
3. Apply basic noise filtering
4. Understand proprioception in robots

Sensors are how robots perceive their environment and their own body state.
"""

import pybullet as p
import pybullet_data
import math
from collections import deque
from typing import List, Tuple


class MovingAverageFilter:
    """
    Simple moving average filter for noisy sensor data.

    This is one of the simplest noise reduction techniques:
    average the last N readings to smooth out random noise.
    """

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)

    def update(self, value: float) -> float:
        """Add a new value and return the filtered result."""
        self.values.append(value)
        return sum(self.values) / len(self.values)


def get_joint_positions(robot_id: int) -> List[Tuple[int, float, float]]:
    """
    Read all joint positions from a robot.

    Returns:
        List of (joint_index, position, velocity) tuples
    """
    num_joints = p.getNumJoints(robot_id)
    joint_states = []

    for i in range(num_joints):
        state = p.getJointState(robot_id, i)
        position = state[0]  # Joint position (radians for revolute, meters for prismatic)
        velocity = state[1]  # Joint velocity
        joint_states.append((i, position, velocity))

    return joint_states


def simulate_distance_sensor(
    robot_id: int,
    sensor_link: int,
    max_range: float = 10.0
) -> Tuple[float, bool]:
    """
    Simulate a simple distance sensor using ray casting.

    Args:
        robot_id: The robot body ID
        sensor_link: Link index where the sensor is mounted
        max_range: Maximum sensing distance in meters

    Returns:
        (distance, hit) where hit is True if something was detected
    """
    # Get the sensor position and orientation from the link
    link_state = p.getLinkState(robot_id, sensor_link)
    sensor_pos = link_state[0]  # World position
    sensor_orn = link_state[1]  # World orientation (quaternion)

    # Convert quaternion to rotation matrix to get forward direction
    rotation_matrix = p.getMatrixFromQuaternion(sensor_orn)
    forward = [rotation_matrix[0], rotation_matrix[3], rotation_matrix[6]]

    # Ray end point
    ray_end = [
        sensor_pos[0] + forward[0] * max_range,
        sensor_pos[1] + forward[1] * max_range,
        sensor_pos[2] + forward[2] * max_range
    ]

    # Cast the ray
    result = p.rayTest(sensor_pos, ray_end)[0]
    hit_object_id = result[0]
    hit_fraction = result[2]

    if hit_object_id >= 0 and hit_object_id != robot_id:
        distance = hit_fraction * max_range
        return (distance, True)
    else:
        return (max_range, False)


def run_sensor_demo(use_gui: bool = True, duration: float = 5.0) -> dict:
    """
    Run a demonstration of robot sensors.

    Args:
        use_gui: If True, opens a visualization window
        duration: How long to run the simulation

    Returns:
        dict with sensor readings history
    """
    # Setup
    physics_client = p.connect(p.GUI if use_gui else p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)

    # Load environment
    plane_id = p.loadURDF("plane.urdf")
    robot_id = p.loadURDF("r2d2.urdf", [0, 0, 0.5])

    # Create a filter for smoothing sensor data
    position_filter = MovingAverageFilter(window_size=10)

    # Simulation
    time_step = 1.0 / 240.0
    steps = int(duration / time_step)

    joint_history = []
    filtered_history = []

    for step in range(steps):
        p.stepSimulation()

        # Read joint sensors every 24 steps (10 Hz sensing rate)
        if step % 24 == 0:
            joint_states = get_joint_positions(robot_id)
            if joint_states:
                # Get first joint position
                raw_position = joint_states[0][1]

                # Add simulated noise
                import random
                noisy_position = raw_position + random.gauss(0, 0.01)

                # Filter the noisy reading
                filtered_position = position_filter.update(noisy_position)

                joint_history.append(noisy_position)
                filtered_history.append(filtered_position)

    p.disconnect()

    return {
        "raw_readings": joint_history,
        "filtered_readings": filtered_history,
        "steps_simulated": steps
    }


if __name__ == "__main__":
    print("Sensor Basics Demo")
    print("=" * 40)
    print()
    print("This demo shows:")
    print("  - Reading joint position sensors")
    print("  - Applying noise filtering")
    print()

    result = run_sensor_demo(use_gui=True, duration=3.0)

    print(f"Collected {len(result['raw_readings'])} sensor readings")

    if result['raw_readings']:
        import statistics
        raw_std = statistics.stdev(result['raw_readings'])
        filtered_std = statistics.stdev(result['filtered_readings'])
        print(f"Raw data std dev:      {raw_std:.4f}")
        print(f"Filtered data std dev: {filtered_std:.4f}")
        print(f"Noise reduction:       {(1 - filtered_std/raw_std)*100:.1f}%")
