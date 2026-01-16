"""
Chapter 1: Hello PyBullet

This example demonstrates how to:
1. Connect to the PyBullet physics engine
2. Load a ground plane and a robot
3. Run a simple simulation loop
4. Properly disconnect when done

This is your first step into Physical AI!
"""

import pybullet as p
import pybullet_data
import time


def run_hello_pybullet(use_gui: bool = True, duration: float = 5.0) -> dict:
    """
    Run a basic PyBullet simulation with a robot.

    Args:
        use_gui: If True, opens a visualization window. If False, runs headless.
        duration: How long to run the simulation in seconds.

    Returns:
        dict with simulation results (robot position, steps taken)
    """
    # Connect to physics engine
    # p.GUI shows a window, p.DIRECT runs headless (for testing)
    physics_client = p.connect(p.GUI if use_gui else p.DIRECT)

    # Tell PyBullet where to find built-in models (planes, robots, etc.)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # Set up gravity (Earth gravity is -9.81 m/s^2 in the Z direction)
    p.setGravity(0, 0, -9.81)

    # Load the ground plane
    plane_id = p.loadURDF("plane.urdf")

    # Load the R2D2 robot 1 meter above the ground
    robot_start_position = [0, 0, 1]
    robot_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
    robot_id = p.loadURDF(
        "r2d2.urdf",
        robot_start_position,
        robot_start_orientation
    )

    # Simulation parameters
    time_step = 1.0 / 240.0  # 240 Hz physics
    steps = int(duration / time_step)

    # Run the simulation
    for step in range(steps):
        p.stepSimulation()

        if use_gui:
            # Slow down to real-time for visualization
            time.sleep(time_step)

    # Get final robot position
    final_position, final_orientation = p.getBasePositionAndOrientation(robot_id)

    # Clean up
    p.disconnect()

    return {
        "final_position": final_position,
        "final_orientation": final_orientation,
        "steps_simulated": steps,
        "robot_id": robot_id,
        "plane_id": plane_id
    }


if __name__ == "__main__":
    print("Starting PyBullet simulation...")
    print("Watch the R2D2 robot fall and settle on the ground plane.")
    print()

    result = run_hello_pybullet(use_gui=True, duration=5.0)

    print(f"Simulation complete!")
    print(f"  Steps simulated: {result['steps_simulated']}")
    print(f"  Final position: {result['final_position']}")
