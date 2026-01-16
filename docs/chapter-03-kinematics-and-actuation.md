---
sidebar_position: 3
title: "Chapter 3: Kinematics and Actuation"
description: "The mathematics of robot motion and how to control physical movement through actuators"
keywords: [kinematics, actuation, motors, control systems, forward kinematics, inverse kinematics]
---

# Chapter 3: Kinematics and Actuation

**Estimated Time**: 4-5 hours
**Prerequisites**: Chapter 1-2 completion, basic calculus concepts (derivatives, integrals)

## Learning Outcomes

By the end of this chapter, you will be able to:

- Explain forward and inverse kinematics for robotic systems
- Describe different actuator types and their appropriate applications
- Implement basic motion control algorithms
- Design feedback control loops for precise movement

---

## 3.1 Introduction to Robot Motion

### What is Kinematics?

Kinematics is the study of motion without considering the forces that cause it. For robots, kinematics answers two fundamental questions:

1. **Forward kinematics**: Given joint angles, where is the end-effector?
2. **Inverse kinematics**: Given a desired end-effector position, what joint angles achieve it?

### Coordinate Frames

Robots use multiple coordinate frames to describe positions and orientations:

- **World frame**: Fixed reference for the environment
- **Base frame**: Attached to the robot's base
- **Joint frames**: Attached to each link of the robot
- **End-effector frame**: At the tool or gripper

### Degrees of Freedom

A robot's **degrees of freedom (DOF)** describe how many independent ways it can move:

- **Translation**: Movement along x, y, z axes (3 DOF)
- **Rotation**: Rotation around x, y, z axes (3 DOF)
- **Full 6-DOF**: Complete position and orientation control

Common robot configurations:

| Robot Type | Typical DOF | Application |
|------------|-------------|-------------|
| Mobile robot (ground) | 2-3 | Navigation |
| Robot arm | 6-7 | Manipulation |
| Quadcopter | 6 | Aerial tasks |
| Humanoid | 20-50+ | General purpose |

---

## 3.2 Forward Kinematics

### The Forward Kinematics Problem

Given: Joint angles (q1, q2, ..., qn)
Find: End-effector position and orientation

### Transformation Matrices

Each link transformation combines rotation and translation:

```python
import numpy as np

def rotation_z(theta):
    """Rotation matrix around z-axis."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])

def translation(dx, dy, dz):
    """Translation matrix."""
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])
```

### Denavit-Hartenberg Parameters

The DH convention provides a systematic way to describe robot geometry:

| Parameter | Description |
|-----------|-------------|
| a (link length) | Distance along x-axis |
| alpha (link twist) | Rotation around x-axis |
| d (link offset) | Distance along z-axis |
| theta (joint angle) | Rotation around z-axis |

```python
def dh_transform(a, alpha, d, theta):
    """Compute transformation matrix from DH parameters."""
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)

    return np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,   sa,     ca,    d   ],
        [0,   0,      0,     1   ]
    ])
```

### Example: 2-Link Planar Arm

```python
def forward_kinematics_2link(q1, q2, L1, L2):
    """
    Forward kinematics for a 2-link planar arm.

    Args:
        q1, q2: Joint angles (radians)
        L1, L2: Link lengths

    Returns:
        (x, y): End-effector position
    """
    x = L1 * np.cos(q1) + L2 * np.cos(q1 + q2)
    y = L1 * np.sin(q1) + L2 * np.sin(q1 + q2)
    return x, y
```

---

## 3.3 Inverse Kinematics

### The Inverse Kinematics Problem

Given: Desired end-effector position and orientation
Find: Joint angles that achieve it

### Challenges of Inverse Kinematics

- **Multiple solutions**: Many joint configurations may reach the same point
- **No solution**: Target may be unreachable
- **Singularities**: Configurations where the robot loses DOF
- **Non-linear equations**: Analytical solutions are difficult for complex robots

### Analytical Solution (2-Link Arm)

```python
def inverse_kinematics_2link(x, y, L1, L2):
    """
    Inverse kinematics for a 2-link planar arm.

    Returns two possible solutions (elbow up and elbow down).
    """
    # Distance to target
    r = np.sqrt(x**2 + y**2)

    # Check reachability
    if r > L1 + L2 or r < abs(L1 - L2):
        return None  # Unreachable

    # Cosine law for q2
    cos_q2 = (r**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_q2 = np.clip(cos_q2, -1, 1)  # Handle numerical errors

    # Two solutions: elbow up and elbow down
    q2_up = np.arccos(cos_q2)
    q2_down = -np.arccos(cos_q2)

    # Solve for q1
    def solve_q1(q2):
        beta = np.arctan2(L2 * np.sin(q2), L1 + L2 * np.cos(q2))
        q1 = np.arctan2(y, x) - beta
        return q1

    solution_up = (solve_q1(q2_up), q2_up)
    solution_down = (solve_q1(q2_down), q2_down)

    return solution_up, solution_down
```

### Numerical Methods

For complex robots, numerical methods find solutions iteratively:

```python
def jacobian_inverse_kinematics(target_pos, initial_joints, forward_kin, jacobian_func,
                                 max_iterations=100, tolerance=0.001):
    """
    Iterative inverse kinematics using the Jacobian.
    """
    joints = initial_joints.copy()

    for iteration in range(max_iterations):
        # Current end-effector position
        current_pos = forward_kin(joints)

        # Error to target
        error = target_pos - current_pos

        # Check convergence
        if np.linalg.norm(error) < tolerance:
            return joints

        # Compute Jacobian
        J = jacobian_func(joints)

        # Compute joint velocity (pseudoinverse for redundant robots)
        J_pinv = np.linalg.pinv(J)
        delta_joints = J_pinv @ error

        # Update joints
        joints = joints + 0.1 * delta_joints  # Step size of 0.1

    return joints  # Return best effort if not converged
```

---

## 3.4 Actuators and Motors

### Types of Actuators

#### Electric Motors

**DC Motors**: Simple, widely used
- Pros: Inexpensive, easy to control
- Cons: Requires gearbox for high torque

**Brushless DC (BLDC)**: Higher efficiency
- Pros: Long life, high power density
- Cons: More complex control

**Servo Motors**: Built-in feedback and control
- Pros: Precise positioning
- Cons: Limited rotation range (typically)

**Stepper Motors**: Discrete steps
- Pros: Open-loop position control
- Cons: Lower torque at high speeds

#### Hydraulic Actuators

- Pros: Very high force, good for heavy-duty applications
- Cons: Complex plumbing, potential for leaks, slow

#### Pneumatic Actuators

- Pros: Fast, compliant, lightweight
- Cons: Difficult to control precisely, noisy

### Motor Specifications

Key parameters when selecting motors:

| Specification | Description |
|---------------|-------------|
| Torque | Rotational force (N-m) |
| Speed | Rotational velocity (RPM) |
| Power | Torque x Speed (Watts) |
| Gear ratio | Input/output speed ratio |
| Encoder resolution | Ticks per revolution |

---

## 3.5 Control Systems

### Open-Loop vs Closed-Loop Control

**Open-loop**: Commands sent without feedback
- Example: Stepper motor moving fixed steps
- Problem: Errors accumulate, no correction

**Closed-loop**: Feedback corrects errors
- Example: Motor with encoder measuring actual position
- Benefit: Maintains accuracy despite disturbances

### PID Control

The PID controller is the most common feedback controller:

```python
class PIDController:
    """Proportional-Integral-Derivative controller."""

    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain

        self.integral = 0
        self.previous_error = 0

    def update(self, setpoint, measured, dt):
        """
        Compute control output.

        Args:
            setpoint: Desired value
            measured: Actual measured value
            dt: Time step

        Returns:
            Control signal
        """
        error = setpoint - measured

        # Proportional term
        P = self.Kp * error

        # Integral term (accumulated error)
        self.integral += error * dt
        I = self.Ki * self.integral

        # Derivative term (rate of change)
        derivative = (error - self.previous_error) / dt
        D = self.Kd * derivative

        self.previous_error = error

        return P + I + D
```

### Tuning PID Controllers

| Gain | Effect if Too Low | Effect if Too High |
|------|-------------------|-------------------|
| Kp | Slow response | Overshoot, oscillation |
| Ki | Steady-state error | Windup, instability |
| Kd | Slow settling | Noise amplification |

**Ziegler-Nichols method**:
1. Set Ki = Kd = 0
2. Increase Kp until oscillation occurs (Ku)
3. Measure oscillation period (Tu)
4. Calculate: Kp = 0.6*Ku, Ki = 2*Kp/Tu, Kd = Kp*Tu/8

---

## 3.6 Motion Planning Basics

### Path vs Trajectory

- **Path**: Sequence of positions (no time information)
- **Trajectory**: Path with timing (velocity profile)

### Trajectory Generation

```python
def trapezoidal_velocity_profile(start, end, max_vel, max_acc, dt):
    """
    Generate a trajectory with trapezoidal velocity profile.

    Returns:
        times, positions, velocities
    """
    distance = end - start
    direction = np.sign(distance)
    distance = abs(distance)

    # Time to accelerate to max velocity
    t_acc = max_vel / max_acc

    # Distance covered during acceleration
    d_acc = 0.5 * max_acc * t_acc**2

    if 2 * d_acc > distance:
        # Triangle profile (never reach max velocity)
        t_acc = np.sqrt(distance / max_acc)
        t_cruise = 0
    else:
        # Trapezoidal profile
        d_cruise = distance - 2 * d_acc
        t_cruise = d_cruise / max_vel

    total_time = 2 * t_acc + t_cruise

    # Generate trajectory points
    times = np.arange(0, total_time, dt)
    positions = []
    velocities = []

    for t in times:
        if t < t_acc:
            # Acceleration phase
            v = max_acc * t
            p = 0.5 * max_acc * t**2
        elif t < t_acc + t_cruise:
            # Cruise phase
            v = max_vel
            p = d_acc + max_vel * (t - t_acc)
        else:
            # Deceleration phase
            t_dec = t - t_acc - t_cruise
            v = max_vel - max_acc * t_dec
            p = d_acc + max_vel * t_cruise + max_vel * t_dec - 0.5 * max_acc * t_dec**2

        positions.append(start + direction * p)
        velocities.append(direction * v)

    return times, np.array(positions), np.array(velocities)
```

---

## Hands-On Exercises

### Exercise 3.1: Forward Kinematics Visualization

1. Create a PyBullet simulation with a multi-joint robot arm
2. Implement forward kinematics using transformation matrices
3. Verify your calculations match the simulated end-effector position
4. Visualize the robot's workspace by sampling joint angles

### Exercise 3.2: Inverse Kinematics Implementation

1. Implement analytical IK for a 2-link planar arm
2. Visualize both elbow-up and elbow-down solutions
3. Implement numerical IK using the Jacobian method
4. Compare convergence speed and accuracy

### Exercise 3.3: PID Motor Control

1. Set up a simulated motor with position feedback
2. Implement a PID controller
3. Tune the gains using the Ziegler-Nichols method
4. Test response to step inputs and disturbances

### Exercise 3.4: Trajectory Following

1. Generate a trapezoidal velocity profile trajectory
2. Command a simulated robot to follow the trajectory
3. Plot commanded vs actual position over time
4. Experiment with different max velocity and acceleration limits

---

## Summary

In this chapter, you learned:

- **Kinematics** describes robot motion mathematically
- **Forward kinematics** computes end-effector pose from joint angles
- **Inverse kinematics** finds joint angles for a desired pose
- **Actuators** convert electrical signals to physical motion
- **PID control** provides feedback-based precision
- **Trajectory generation** plans motion with time constraints

---

## Key Terms

- **Degrees of Freedom (DOF)**: Number of independent motion parameters
- **Forward Kinematics**: Joint angles to end-effector pose
- **Inverse Kinematics**: End-effector pose to joint angles
- **Jacobian**: Matrix relating joint velocities to end-effector velocity
- **PID Controller**: Proportional-Integral-Derivative feedback controller
- **Trajectory**: Path with associated timing information

---

## Next Chapter Preview

In Chapter 4, you will learn about **Cognitive Architectures for Humanoids**—how to integrate perception, planning, and action into coherent intelligent systems, with special considerations for human-like robots.
