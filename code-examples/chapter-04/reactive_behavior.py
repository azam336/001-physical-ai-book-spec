"""
Chapter 4: Reactive Behavior

This example demonstrates:
1. Simple reactive (stimulus-response) behavior
2. Braitenberg vehicles (light-seeking behavior)
3. Subsumption architecture basics
4. Layered behavior priorities

Reactive architectures directly map sensor inputs to motor outputs
without explicit world models or planning.
"""

import pybullet as p
import pybullet_data
import math
import time
from typing import Tuple, List, Callable
from dataclasses import dataclass


@dataclass
class BehaviorOutput:
    """Output from a behavior layer."""
    left_velocity: float
    right_velocity: float
    active: bool = False


class BraitenbergVehicle:
    """
    Implementation of Braitenberg Vehicle 2a (fear/attraction).

    Braitenberg vehicles are simple reactive robots that exhibit
    seemingly complex behaviors from very simple sensor-motor mappings.

    Vehicle 2a: Crossed connections -> attracted to light source
    Vehicle 2b: Parallel connections -> repelled by light source
    """

    def __init__(
        self,
        robot_id: int,
        left_wheel_joint: int,
        right_wheel_joint: int,
        crossed: bool = True
    ):
        self.robot_id = robot_id
        self.left_wheel = left_wheel_joint
        self.right_wheel = right_wheel_joint
        self.crossed = crossed  # True = attraction, False = fear
        self.max_velocity = 10.0

    def sense_light(self, light_position: Tuple[float, float, float]) -> Tuple[float, float]:
        """
        Simulate left and right light sensors.

        Returns intensity values for left and right sensors based on
        the angle to the light source.
        """
        # Get robot position and orientation
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)

        # Vector to light
        to_light = [
            light_position[0] - pos[0],
            light_position[1] - pos[1]
        ]

        # Distance to light (inverse square for intensity)
        distance = math.sqrt(to_light[0]**2 + to_light[1]**2)
        if distance < 0.1:
            distance = 0.1

        # Robot heading (yaw angle)
        euler = p.getEulerFromQuaternion(orn)
        heading = euler[2]

        # Angle to light relative to robot heading
        angle_to_light = math.atan2(to_light[1], to_light[0]) - heading

        # Simulate left and right sensors at +/- 30 degrees
        left_sensor_angle = angle_to_light - math.radians(30)
        right_sensor_angle = angle_to_light + math.radians(30)

        # Sensor response (cosine falloff, clamped to positive values)
        left_intensity = max(0, math.cos(left_sensor_angle)) / (distance**2)
        right_intensity = max(0, math.cos(right_sensor_angle)) / (distance**2)

        return (left_intensity, right_intensity)

    def compute_wheel_velocities(
        self,
        light_position: Tuple[float, float, float]
    ) -> Tuple[float, float]:
        """
        Compute wheel velocities based on light sensor readings.

        This is the core Braitenberg behavior: direct sensor-motor mapping.
        """
        left_sensor, right_sensor = self.sense_light(light_position)

        if self.crossed:
            # Vehicle 2a: crossed connections (attraction)
            # Left sensor -> right wheel, right sensor -> left wheel
            left_velocity = right_sensor * self.max_velocity
            right_velocity = left_sensor * self.max_velocity
        else:
            # Vehicle 2b: parallel connections (fear/avoidance)
            # Left sensor -> left wheel, right sensor -> right wheel
            left_velocity = left_sensor * self.max_velocity
            right_velocity = right_sensor * self.max_velocity

        return (left_velocity, right_velocity)

    def step(self, light_position: Tuple[float, float, float]) -> None:
        """Execute one step of the Braitenberg behavior."""
        left_vel, right_vel = self.compute_wheel_velocities(light_position)

        # Apply velocities to wheels
        p.setJointMotorControl2(
            self.robot_id,
            self.left_wheel,
            p.VELOCITY_CONTROL,
            targetVelocity=left_vel,
            force=100
        )
        p.setJointMotorControl2(
            self.robot_id,
            self.right_wheel,
            p.VELOCITY_CONTROL,
            targetVelocity=right_vel,
            force=100
        )


class SubsumptionController:
    """
    Simple subsumption architecture implementation.

    Higher priority behaviors can suppress (subsume) lower priority ones.
    This creates layered reactive control where safety behaviors
    take precedence over goal-seeking behaviors.
    """

    def __init__(self):
        self.behaviors: List[Tuple[int, Callable[[], BehaviorOutput]]] = []

    def add_behavior(self, priority: int, behavior_fn: Callable[[], BehaviorOutput]) -> None:
        """Add a behavior with given priority (higher = more important)."""
        self.behaviors.append((priority, behavior_fn))
        self.behaviors.sort(key=lambda x: x[0], reverse=True)

    def compute(self) -> BehaviorOutput:
        """
        Run all behaviors and return output from highest priority active behavior.
        """
        for priority, behavior_fn in self.behaviors:
            output = behavior_fn()
            if output.active:
                return output

        # Default: no behavior active
        return BehaviorOutput(0, 0, False)


def run_braitenberg_demo(use_gui: bool = True, duration: float = 10.0) -> dict:
    """
    Run a Braitenberg vehicle demonstration.

    The robot will be attracted to a light source (visual marker).
    """
    # Setup
    physics_client = p.connect(p.GUI if use_gui else p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)

    # Load environment
    plane_id = p.loadURDF("plane.urdf")

    # Load a simple wheeled robot
    robot_id = p.loadURDF("husky/husky.urdf", [0, 0, 0.1])

    # Find wheel joints (Husky has 4 wheels)
    num_joints = p.getNumJoints(robot_id)
    wheel_joints = []
    for i in range(num_joints):
        joint_info = p.getJointInfo(robot_id, i)
        if b"wheel" in joint_info[1].lower():
            wheel_joints.append(i)

    # Use front wheels for differential drive approximation
    left_wheel = wheel_joints[0] if len(wheel_joints) > 0 else 0
    right_wheel = wheel_joints[1] if len(wheel_joints) > 1 else 1

    # Create light source position (goal)
    light_position = [3.0, 2.0, 0.5]

    # Create visual marker for light
    if use_gui:
        visual_id = p.createVisualShape(
            p.GEOM_SPHERE,
            radius=0.2,
            rgbaColor=[1, 1, 0, 1]  # Yellow
        )
        light_marker = p.createMultiBody(
            baseVisualShapeIndex=visual_id,
            basePosition=light_position
        )

    # Create Braitenberg controller
    vehicle = BraitenbergVehicle(
        robot_id,
        left_wheel,
        right_wheel,
        crossed=True  # Attraction behavior
    )

    # Simulation
    time_step = 1.0 / 240.0
    steps = int(duration / time_step)
    trajectory = []

    for step in range(steps):
        # Run behavior
        vehicle.step(light_position)

        p.stepSimulation()

        # Record trajectory every 24 steps
        if step % 24 == 0:
            pos, _ = p.getBasePositionAndOrientation(robot_id)
            trajectory.append(pos)

        if use_gui:
            time.sleep(time_step)

    # Final position
    final_pos, _ = p.getBasePositionAndOrientation(robot_id)
    distance_to_light = math.sqrt(
        (final_pos[0] - light_position[0])**2 +
        (final_pos[1] - light_position[1])**2
    )

    p.disconnect()

    return {
        "trajectory": trajectory,
        "final_position": final_pos,
        "light_position": light_position,
        "distance_to_light": distance_to_light
    }


if __name__ == "__main__":
    print("Braitenberg Vehicle Demo")
    print("=" * 40)
    print()
    print("A simple reactive robot that is attracted to a light source.")
    print("Watch as it navigates toward the yellow sphere!")
    print()

    result = run_braitenberg_demo(use_gui=True, duration=10.0)

    print(f"\nResults:")
    print(f"  Light position:     {result['light_position']}")
    print(f"  Final position:     [{result['final_position'][0]:.2f}, "
          f"{result['final_position'][1]:.2f}]")
    print(f"  Distance to light:  {result['distance_to_light']:.2f} meters")
    print(f"  Trajectory points:  {len(result['trajectory'])}")
