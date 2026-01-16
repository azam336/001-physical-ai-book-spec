---
sidebar_position: 10
title: Glossary
description: Definitions of key terms used throughout the Physical AI book
keywords: [glossary, definitions, physical ai, robotics, terminology]
---

# Glossary

This glossary defines key terms used throughout the book. Terms are organized alphabetically.

---

## A

### Actuation {#actuation}

**Definition**: The process of converting control signals into physical movement through motors, servos, or other actuators.

**Related**: [Actuator](#actuator), [Control System](#control-system)

**Used in**: Chapters 1, 3

### Actuator {#actuator}

**Definition**: A mechanical device that converts energy (electrical, hydraulic, pneumatic) into physical motion.

**Related**: [Motor](#motor), [Servo](#servo), [Actuation](#actuation)

**Used in**: Chapters 1, 3

---

## C

### Cognitive Architecture {#cognitive-architecture}

**Definition**: The overall structure of an intelligent system that integrates perception, reasoning, learning, and action.

**Related**: [Deliberative Architecture](#deliberative-architecture), [Reactive Architecture](#reactive-architecture)

**Used in**: Chapter 4

### Control System {#control-system}

**Definition**: A system that manages, commands, directs, or regulates the behavior of other systems or processes.

**Related**: [PID Controller](#pid-controller), [Feedback Loop](#feedback-loop)

**Used in**: Chapter 3

---

## D

### Degrees of Freedom (DOF) {#degrees-of-freedom}

**Definition**: The number of independent parameters that define a system's configuration. A robot arm typically has 6-7 DOF.

**Related**: [Kinematics](#kinematics), [Joint](#joint)

**Used in**: Chapter 3

### Deliberative Architecture {#deliberative-architecture}

**Definition**: A cognitive architecture that maintains explicit world models and uses planning algorithms to decide actions.

**Related**: [Cognitive Architecture](#cognitive-architecture), [Reactive Architecture](#reactive-architecture)

**Used in**: Chapter 4

---

## E

### Embodied AI {#embodied-ai}

**Definition**: AI systems with physical presence that interact with the real world through sensors and actuators.

**Related**: [Physical AI](#physical-ai), [Embodiment Hypothesis](#embodiment-hypothesis)

**Used in**: Chapter 1

### Embodiment Hypothesis {#embodiment-hypothesis}

**Definition**: The theory that true intelligence requires a physical body and emerges from continuous interaction between an agent and its environment.

**Related**: [Embodied AI](#embodied-ai)

**Used in**: Chapter 1

---

## F

### Feedback Loop {#feedback-loop}

**Definition**: A control mechanism where output is measured and compared to desired state, with corrections applied continuously.

**Related**: [PID Controller](#pid-controller), [Control System](#control-system)

**Used in**: Chapter 3

### Forward Kinematics {#forward-kinematics}

**Definition**: Computing the end-effector position and orientation given the joint angles of a robot.

**Related**: [Inverse Kinematics](#inverse-kinematics), [Kinematics](#kinematics)

**Used in**: Chapter 3

---

## I

### IMU (Inertial Measurement Unit) {#imu}

**Definition**: A sensor device that measures acceleration (accelerometer) and rotation rate (gyroscope), often with a magnetometer for heading.

**Related**: [Sensor](#sensor), [Proprioception](#proprioception)

**Used in**: Chapter 2

### Inverse Kinematics {#inverse-kinematics}

**Definition**: Computing the joint angles required to achieve a desired end-effector position and orientation.

**Related**: [Forward Kinematics](#forward-kinematics), [Kinematics](#kinematics)

**Used in**: Chapter 3

---

## J

### Jacobian {#jacobian}

**Definition**: A matrix that relates joint velocities to end-effector velocity, used in inverse kinematics and control.

**Related**: [Inverse Kinematics](#inverse-kinematics)

**Used in**: Chapter 3

### Joint {#joint}

**Definition**: A connection between two robot links that allows relative motion (revolute for rotation, prismatic for translation).

**Related**: [Degrees of Freedom](#degrees-of-freedom)

**Used in**: Chapter 3

---

## K

### Kalman Filter {#kalman-filter}

**Definition**: An optimal state estimation algorithm for linear systems with Gaussian noise, widely used in robotics for sensor fusion.

**Related**: [Sensor Fusion](#sensor-fusion)

**Used in**: Chapter 2

### Kinematics {#kinematics}

**Definition**: The study of motion without considering forces, describing relationships between joint positions and end-effector pose.

**Related**: [Forward Kinematics](#forward-kinematics), [Inverse Kinematics](#inverse-kinematics)

**Used in**: Chapter 3

---

## L

### LIDAR {#lidar}

**Definition**: Light Detection and Ranging—a sensor that uses laser pulses to measure distances and create 3D point clouds.

**Related**: [Point Cloud](#point-cloud), [Sensor](#sensor)

**Used in**: Chapter 2

---

## M

### Motor {#motor}

**Definition**: An electrical device that converts electrical energy into rotational mechanical energy.

**Related**: [Actuator](#actuator), [Servo](#servo)

**Used in**: Chapters 1, 3

---

## P

### Perception {#perception}

**Definition**: The process of gathering, processing, and interpreting sensor data to understand the environment.

**Related**: [Sensor](#sensor), [Computer Vision](#computer-vision)

**Used in**: Chapters 1, 2

### Physical AI {#physical-ai}

**Definition**: AI systems that interact with the physical world through sensors and actuators (synonym for Embodied AI).

**Related**: [Embodied AI](#embodied-ai)

**Used in**: All chapters

### PID Controller {#pid-controller}

**Definition**: A feedback controller that uses Proportional, Integral, and Derivative terms to minimize error between desired and actual state.

**Related**: [Control System](#control-system), [Feedback Loop](#feedback-loop)

**Used in**: Chapter 3

### Planning {#planning}

**Definition**: The process of deciding what actions to take to achieve a goal, including path planning and task planning.

**Related**: [Perception](#perception), [Actuation](#actuation)

**Used in**: Chapters 1, 4

### Point Cloud {#point-cloud}

**Definition**: A set of 3D points representing surfaces in the environment, typically generated by LIDAR or depth cameras.

**Related**: [LIDAR](#lidar)

**Used in**: Chapter 2

### Proprioception {#proprioception}

**Definition**: A robot's sense of its own body state, including joint positions, velocities, and forces.

**Related**: [IMU](#imu), [Sensor](#sensor)

**Used in**: Chapter 2

---

## R

### Reactive Architecture {#reactive-architecture}

**Definition**: A cognitive architecture that directly maps sensor inputs to motor outputs without explicit world models.

**Related**: [Cognitive Architecture](#cognitive-architecture), [Subsumption Architecture](#subsumption-architecture)

**Used in**: Chapter 4

### Reinforcement Learning {#reinforcement-learning}

**Definition**: A machine learning approach where agents learn by trial and error, receiving rewards for desired behaviors.

**Related**: [Q-Learning](#q-learning)

**Used in**: Chapter 4

---

## S

### Sensor {#sensor}

**Definition**: A device that detects physical properties (light, distance, force, etc.) and converts them to signals a robot can process.

**Related**: [Perception](#perception), [LIDAR](#lidar), [IMU](#imu)

**Used in**: Chapters 1, 2

### Sensor Fusion {#sensor-fusion}

**Definition**: Combining data from multiple sensors to achieve better perception than any single sensor alone.

**Related**: [Kalman Filter](#kalman-filter), [Perception](#perception)

**Used in**: Chapter 2

### Servo {#servo}

**Definition**: A motor with integrated position feedback and control, commonly used for precise positioning in robotics.

**Related**: [Motor](#motor), [Actuator](#actuator)

**Used in**: Chapter 3

### Simulation {#simulation}

**Definition**: A virtual environment that models physical properties (gravity, collisions, friction) for testing robot software without hardware.

**Related**: [Sim-to-Real Gap](#sim-to-real-gap)

**Used in**: Chapter 1

### Sim-to-Real Gap {#sim-to-real-gap}

**Definition**: The difference between simulated and real-world behavior that can cause policies trained in simulation to fail on real robots.

**Related**: [Simulation](#simulation)

**Used in**: Chapter 1

### Subsumption Architecture {#subsumption-architecture}

**Definition**: A reactive architecture organizing behaviors in layers where higher layers can suppress lower layers.

**Related**: [Reactive Architecture](#reactive-architecture)

**Used in**: Chapter 4

---

## U

### URDF {#urdf}

**Definition**: Unified Robot Description Format—an XML format for describing robot geometry, kinematics, and dynamics.

**Related**: [Simulation](#simulation)

**Used in**: Chapter 1

---

## Z

### Zero Moment Point (ZMP) {#zmp}

**Definition**: A point on the ground where the total reaction force produces no moment in the horizontal plane—used for bipedal balance.

**Related**: [Balance](#balance)

**Used in**: Chapter 4
