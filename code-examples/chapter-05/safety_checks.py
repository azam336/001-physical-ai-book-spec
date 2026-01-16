"""
Chapter 5: Safety Checks

This example demonstrates:
1. Workspace boundary monitoring
2. Joint limit checking
3. Velocity limit enforcement
4. Emergency stop functionality
5. Safety envelope concepts

Safety is critical in Physical AI - robots must protect humans,
themselves, and their environment.
"""

import pybullet as p
import pybullet_data
import math
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class SafetyLevel(Enum):
    """Safety alert levels."""
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class SafetyStatus:
    """Current safety status of the robot."""
    level: SafetyLevel
    message: str
    joint_violations: List[int]
    workspace_violation: bool
    velocity_violations: List[int]


class SafetyMonitor:
    """
    Monitors robot safety and enforces limits.

    This is a simplified version of industrial safety systems.
    Real systems include hardware interlocks, redundant sensors,
    and certified safety PLCs.
    """

    def __init__(
        self,
        robot_id: int,
        workspace_bounds: Tuple[Tuple[float, float, float], Tuple[float, float, float]],
        max_joint_velocity: float = 2.0,
        joint_limit_margin: float = 0.1
    ):
        """
        Initialize safety monitor.

        Args:
            robot_id: PyBullet robot ID
            workspace_bounds: ((min_x, min_y, min_z), (max_x, max_y, max_z))
            max_joint_velocity: Maximum allowed joint velocity (rad/s)
            joint_limit_margin: Safety margin from joint limits (radians)
        """
        self.robot_id = robot_id
        self.workspace_min = workspace_bounds[0]
        self.workspace_max = workspace_bounds[1]
        self.max_joint_velocity = max_joint_velocity
        self.joint_limit_margin = joint_limit_margin
        self.emergency_stop_active = False

        # Get joint limits from URDF
        self.num_joints = p.getNumJoints(robot_id)
        self.joint_limits = []
        for i in range(self.num_joints):
            info = p.getJointInfo(robot_id, i)
            lower_limit = info[8]
            upper_limit = info[9]
            self.joint_limits.append((lower_limit, upper_limit))

    def check_workspace(self) -> Tuple[bool, Optional[str]]:
        """
        Check if robot is within workspace bounds.

        Returns:
            (is_safe, violation_message)
        """
        # Check end effector position (using last link)
        for link_idx in range(self.num_joints):
            state = p.getLinkState(self.robot_id, link_idx)
            pos = state[0]

            for i, (p_val, min_val, max_val) in enumerate(
                zip(pos, self.workspace_min, self.workspace_max)
            ):
                if p_val < min_val or p_val > max_val:
                    axis = ['X', 'Y', 'Z'][i]
                    return (False, f"Link {link_idx} {axis}={p_val:.2f} outside bounds")

        return (True, None)

    def check_joint_limits(self) -> List[int]:
        """
        Check if any joints are near their limits.

        Returns:
            List of joint indices that are near limits
        """
        violations = []

        for i in range(self.num_joints):
            state = p.getJointState(self.robot_id, i)
            position = state[0]
            lower, upper = self.joint_limits[i]

            # Skip continuous joints (limits are 0, -1)
            if lower >= upper:
                continue

            # Check if within margin of limits
            if (position < lower + self.joint_limit_margin or
                position > upper - self.joint_limit_margin):
                violations.append(i)

        return violations

    def check_velocities(self) -> List[int]:
        """
        Check if any joints exceed velocity limits.

        Returns:
            List of joint indices with velocity violations
        """
        violations = []

        for i in range(self.num_joints):
            state = p.getJointState(self.robot_id, i)
            velocity = abs(state[1])

            if velocity > self.max_joint_velocity:
                violations.append(i)

        return violations

    def get_safety_status(self) -> SafetyStatus:
        """
        Perform all safety checks and return current status.
        """
        if self.emergency_stop_active:
            return SafetyStatus(
                level=SafetyLevel.EMERGENCY,
                message="Emergency stop active",
                joint_violations=[],
                workspace_violation=False,
                velocity_violations=[]
            )

        # Run all checks
        workspace_ok, workspace_msg = self.check_workspace()
        joint_violations = self.check_joint_limits()
        velocity_violations = self.check_velocities()

        # Determine overall level
        if velocity_violations:
            level = SafetyLevel.CRITICAL
            message = f"Velocity limit exceeded on joints: {velocity_violations}"
        elif not workspace_ok:
            level = SafetyLevel.CRITICAL
            message = workspace_msg
        elif joint_violations:
            level = SafetyLevel.WARNING
            message = f"Near joint limits: {joint_violations}"
        else:
            level = SafetyLevel.OK
            message = "All systems nominal"

        return SafetyStatus(
            level=level,
            message=message,
            joint_violations=joint_violations,
            workspace_violation=not workspace_ok,
            velocity_violations=velocity_violations
        )

    def emergency_stop(self) -> None:
        """
        Activate emergency stop - halt all joint motion.
        """
        self.emergency_stop_active = True

        for i in range(self.num_joints):
            # Set velocity to zero with high force
            p.setJointMotorControl2(
                self.robot_id,
                i,
                p.VELOCITY_CONTROL,
                targetVelocity=0,
                force=1000
            )

    def reset_emergency_stop(self) -> None:
        """Reset emergency stop (requires explicit action)."""
        self.emergency_stop_active = False


def run_safety_demo(use_gui: bool = True, duration: float = 5.0) -> dict:
    """
    Demonstrate safety monitoring on a robot arm.
    """
    # Setup
    physics_client = p.connect(p.GUI if use_gui else p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)

    # Load environment
    plane_id = p.loadURDF("plane.urdf")
    robot_id = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)

    # Define workspace bounds (1m cube centered on robot)
    workspace_bounds = (
        (-0.8, -0.8, 0.0),   # min x, y, z
        (0.8, 0.8, 1.2)      # max x, y, z
    )

    # Create safety monitor
    monitor = SafetyMonitor(
        robot_id,
        workspace_bounds,
        max_joint_velocity=1.5,
        joint_limit_margin=0.2
    )

    # Simulation
    time_step = 1.0 / 240.0
    steps = int(duration / time_step)
    safety_log = []

    # Apply some motion to trigger safety events
    num_joints = p.getNumJoints(robot_id)

    for step in range(steps):
        # Apply oscillating motion to first joint
        target = math.sin(step * time_step * 2) * 1.5  # Intentionally near limits

        p.setJointMotorControl2(
            robot_id,
            0,
            p.POSITION_CONTROL,
            targetPosition=target,
            force=200
        )

        p.stepSimulation()

        # Check safety every 24 steps
        if step % 24 == 0:
            status = monitor.get_safety_status()
            safety_log.append({
                "step": step,
                "level": status.level.value,
                "message": status.message
            })

            # Print warnings in real-time
            if use_gui and status.level != SafetyLevel.OK:
                print(f"[{status.level.value.upper()}] {status.message}")

        if use_gui:
            time.sleep(time_step)

    p.disconnect()

    # Count events by level
    level_counts = {}
    for entry in safety_log:
        level = entry["level"]
        level_counts[level] = level_counts.get(level, 0) + 1

    return {
        "safety_log": safety_log,
        "level_counts": level_counts,
        "total_checks": len(safety_log)
    }


if __name__ == "__main__":
    print("Safety Monitoring Demo")
    print("=" * 40)
    print()
    print("This demo shows safety monitoring including:")
    print("  - Workspace boundary checking")
    print("  - Joint limit monitoring")
    print("  - Velocity limit enforcement")
    print()

    result = run_safety_demo(use_gui=True, duration=10.0)

    print(f"\nSafety Check Summary:")
    print(f"  Total checks: {result['total_checks']}")
    for level, count in sorted(result['level_counts'].items()):
        print(f"  {level}: {count}")
