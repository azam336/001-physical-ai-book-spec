"""
Test suite for Physical AI book code examples.

These tests run in headless mode (p.DIRECT) to verify that all
code examples execute correctly without errors.

Run with: pytest code-examples/tests/ -v
"""

import pytest
import sys
import os
import math

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestChapter01:
    """Tests for Chapter 1: Introduction to Embodied AI."""

    def test_hello_pybullet_runs(self):
        """Verify hello_pybullet simulation runs without errors."""
        from chapter_01.hello_pybullet import run_hello_pybullet

        result = run_hello_pybullet(use_gui=False, duration=0.5)

        assert result is not None
        assert "final_position" in result
        assert "steps_simulated" in result
        assert result["steps_simulated"] > 0

    def test_hello_pybullet_robot_falls(self):
        """Verify the robot falls due to gravity."""
        from chapter_01.hello_pybullet import run_hello_pybullet

        result = run_hello_pybullet(use_gui=False, duration=1.0)

        # Robot started at z=1, should have fallen
        final_z = result["final_position"][2]
        assert final_z < 0.9, f"Robot should have fallen, but z={final_z}"


class TestChapter02:
    """Tests for Chapter 2: Sensors and Perception."""

    def test_moving_average_filter(self):
        """Test the moving average filter implementation."""
        from chapter_02.sensor_basics import MovingAverageFilter

        filter = MovingAverageFilter(window_size=3)

        # First value - average of one
        assert filter.update(10.0) == 10.0

        # Second value - average of two
        assert filter.update(20.0) == 15.0

        # Third value - average of three
        assert filter.update(30.0) == 20.0

        # Fourth value - window slides
        result = filter.update(40.0)
        assert result == 30.0  # (20 + 30 + 40) / 3

    def test_sensor_demo_runs(self):
        """Verify sensor demo runs without errors."""
        from chapter_02.sensor_basics import run_sensor_demo

        result = run_sensor_demo(use_gui=False, duration=0.5)

        assert result is not None
        assert "raw_readings" in result
        assert "filtered_readings" in result
        assert len(result["raw_readings"]) > 0


class TestChapter03:
    """Tests for Chapter 3: Kinematics and Actuation."""

    def test_forward_kinematics(self):
        """Test forward kinematics calculation."""
        from chapter_03.inverse_kinematics import forward_kinematics_2link

        # At zero angles, end effector should be at (2, 0)
        x, y = forward_kinematics_2link(0, 0, L1=1.0, L2=1.0)
        assert abs(x - 2.0) < 1e-6
        assert abs(y - 0.0) < 1e-6

        # At 90 degrees for both joints
        x, y = forward_kinematics_2link(math.pi/2, 0, L1=1.0, L2=1.0)
        assert abs(x - 0.0) < 1e-6
        assert abs(y - 2.0) < 1e-6

    def test_inverse_kinematics_reachable(self):
        """Test IK for reachable target."""
        from chapter_03.inverse_kinematics import analytical_2link_ik, forward_kinematics_2link

        # Target at (1.5, 0.5)
        result = analytical_2link_ik(1.5, 0.5)
        assert result is not None

        theta1, theta2 = result

        # Verify with forward kinematics
        x, y = forward_kinematics_2link(theta1, theta2)
        assert abs(x - 1.5) < 1e-4
        assert abs(y - 0.5) < 1e-4

    def test_inverse_kinematics_unreachable(self):
        """Test IK returns None for unreachable target."""
        from chapter_03.inverse_kinematics import analytical_2link_ik

        # Target too far away
        result = analytical_2link_ik(5.0, 0.0)
        assert result is None

    def test_pybullet_ik_demo_runs(self):
        """Verify PyBullet IK demo runs without errors."""
        from chapter_03.inverse_kinematics import run_ik_demo_pybullet

        result = run_ik_demo_pybullet(use_gui=False)

        assert result is not None
        assert "position_error" in result
        # IK should get reasonably close
        assert result["position_error"] < 0.1


class TestChapter04:
    """Tests for Chapter 4: Cognitive Architectures."""

    def test_behavior_output_dataclass(self):
        """Test BehaviorOutput dataclass."""
        from chapter_04.reactive_behavior import BehaviorOutput

        output = BehaviorOutput(left_velocity=1.0, right_velocity=2.0, active=True)

        assert output.left_velocity == 1.0
        assert output.right_velocity == 2.0
        assert output.active is True

    def test_subsumption_controller(self):
        """Test subsumption architecture priority."""
        from chapter_04.reactive_behavior import SubsumptionController, BehaviorOutput

        controller = SubsumptionController()

        # Low priority behavior (always active)
        def low_priority():
            return BehaviorOutput(1.0, 1.0, active=True)

        # High priority behavior (conditionally active)
        high_priority_active = [False]

        def high_priority():
            if high_priority_active[0]:
                return BehaviorOutput(5.0, 5.0, active=True)
            return BehaviorOutput(0, 0, active=False)

        controller.add_behavior(1, low_priority)
        controller.add_behavior(10, high_priority)

        # When high priority is inactive, low priority runs
        result = controller.compute()
        assert result.left_velocity == 1.0

        # When high priority is active, it takes over
        high_priority_active[0] = True
        result = controller.compute()
        assert result.left_velocity == 5.0

    def test_braitenberg_demo_runs(self):
        """Verify Braitenberg demo runs without errors."""
        from chapter_04.reactive_behavior import run_braitenberg_demo

        result = run_braitenberg_demo(use_gui=False, duration=1.0)

        assert result is not None
        assert "trajectory" in result
        assert "distance_to_light" in result
        assert len(result["trajectory"]) > 0


class TestChapter05:
    """Tests for Chapter 5: Safety and Ethics."""

    def test_safety_level_enum(self):
        """Test SafetyLevel enum values."""
        from chapter_05.safety_checks import SafetyLevel

        assert SafetyLevel.OK.value == "ok"
        assert SafetyLevel.WARNING.value == "warning"
        assert SafetyLevel.CRITICAL.value == "critical"
        assert SafetyLevel.EMERGENCY.value == "emergency"

    def test_safety_status_dataclass(self):
        """Test SafetyStatus dataclass."""
        from chapter_05.safety_checks import SafetyStatus, SafetyLevel

        status = SafetyStatus(
            level=SafetyLevel.OK,
            message="All good",
            joint_violations=[],
            workspace_violation=False,
            velocity_violations=[]
        )

        assert status.level == SafetyLevel.OK
        assert status.message == "All good"

    def test_safety_demo_runs(self):
        """Verify safety demo runs without errors."""
        from chapter_05.safety_checks import run_safety_demo

        result = run_safety_demo(use_gui=False, duration=1.0)

        assert result is not None
        assert "safety_log" in result
        assert "level_counts" in result
        assert result["total_checks"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
