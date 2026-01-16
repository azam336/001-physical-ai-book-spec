---
sidebar_position: 4
title: "Chapter 4: Cognitive Architectures for Humanoids"
description: "Integrating perception, planning, and action into coherent cognitive systems for humanoid robots"
keywords: [cognitive architecture, humanoid robots, decision making, learning, AI planning]
---

# Chapter 4: Cognitive Architectures for Humanoids

**Estimated Time**: 4-5 hours
**Prerequisites**: Chapters 1-3 completion, understanding of perception and actuation pipelines

## Learning Outcomes

By the end of this chapter, you will be able to:

- Compare and contrast major cognitive architecture approaches (reactive, deliberative, hybrid)
- Design decision-making systems that handle uncertainty and incomplete information
- Implement learning mechanisms that improve performance over time
- Apply cognitive architecture principles to humanoid robot design

---

## 4.1 What is a Cognitive Architecture?

### The Integration Challenge

In previous chapters, you learned about perception and actuation as separate systems. The central challenge of cognitive architecture is: **How do we integrate these into a coherent, intelligent whole?**

A cognitive architecture provides:

- **Structure**: Organization of processing components
- **Knowledge representation**: How information is stored and accessed
- **Processing mechanisms**: How decisions are made
- **Learning capabilities**: How the system improves over time

### Historical Perspectives

The field has evolved through several paradigms:

| Era | Approach | Key Idea |
|-----|----------|----------|
| 1960s-1980s | Deliberative | Detailed world models, planning |
| 1980s-1990s | Reactive | Direct sensor-action mappings |
| 1990s-present | Hybrid | Combine deliberative and reactive |
| 2010s-present | Learning-based | Neural networks, reinforcement learning |

---

## 4.2 Reactive Architectures

### The Subsumption Architecture

Rodney Brooks proposed the subsumption architecture in the 1980s, arguing that intelligence emerges from simple behaviors layered together.

**Key principles**:
- No central world model
- Behaviors organized in layers
- Higher layers subsume (suppress) lower layers
- Each layer directly connects sensors to actuators

```
┌─────────────────────────────────────┐
│  Layer 2: Explore (wander)          │ Lowest priority
├─────────────────────────────────────┤
│  Layer 1: Avoid obstacles           │
├─────────────────────────────────────┤
│  Layer 0: Emergency stop            │ Highest priority
└─────────────────────────────────────┘
```

### Implementation Example

```python
class ReactiveBehavior:
    """Base class for reactive behaviors."""

    def __init__(self, priority):
        self.priority = priority

    def is_active(self, sensor_data):
        """Return True if this behavior should activate."""
        raise NotImplementedError

    def get_action(self, sensor_data):
        """Return the action for this behavior."""
        raise NotImplementedError


class EmergencyStop(ReactiveBehavior):
    """Highest priority: stop if something is very close."""

    def __init__(self):
        super().__init__(priority=0)

    def is_active(self, sensor_data):
        return sensor_data['min_distance'] < 0.2  # 20cm threshold

    def get_action(self, sensor_data):
        return {'linear_velocity': 0, 'angular_velocity': 0}


class ObstacleAvoidance(ReactiveBehavior):
    """Avoid obstacles by turning away."""

    def __init__(self):
        super().__init__(priority=1)

    def is_active(self, sensor_data):
        return sensor_data['min_distance'] < 1.0

    def get_action(self, sensor_data):
        # Turn away from closest obstacle
        if sensor_data['closest_on_left']:
            return {'linear_velocity': 0.3, 'angular_velocity': -0.5}
        else:
            return {'linear_velocity': 0.3, 'angular_velocity': 0.5}


class SubsumptionController:
    """Controller using subsumption architecture."""

    def __init__(self, behaviors):
        # Sort by priority (lower number = higher priority)
        self.behaviors = sorted(behaviors, key=lambda b: b.priority)

    def get_action(self, sensor_data):
        """Get action from highest priority active behavior."""
        for behavior in self.behaviors:
            if behavior.is_active(sensor_data):
                return behavior.get_action(sensor_data)
        return {'linear_velocity': 0, 'angular_velocity': 0}
```

### Strengths and Limitations

**Strengths**:
- Fast response (no planning overhead)
- Robust to sensor noise
- Easy to understand and debug

**Limitations**:
- Difficult to achieve complex goals
- No lookahead or planning
- Behavior interactions can be unpredictable

---

## 4.3 Deliberative Architectures

### The Planning Approach

Deliberative architectures maintain explicit world models and use planning algorithms to decide actions.

**Key components**:
- **World model**: Representation of environment state
- **Goal representation**: What the robot should achieve
- **Planner**: Algorithm to find action sequences
- **Executor**: Carries out planned actions

### Classical Planning

Classical planning assumes:
- Complete knowledge of initial state
- Deterministic actions
- Goals defined as target states

```python
class ClassicalPlanner:
    """Simple forward-search planner."""

    def __init__(self, actions):
        self.actions = actions

    def plan(self, initial_state, goal_condition, max_depth=10):
        """
        Find a sequence of actions from initial_state to goal.

        Args:
            initial_state: Starting state
            goal_condition: Function returning True if goal is reached
            max_depth: Maximum plan length

        Returns:
            List of actions, or None if no plan found
        """
        from collections import deque

        # Breadth-first search
        queue = deque([(initial_state, [])])
        visited = {initial_state}

        while queue:
            state, plan = queue.popleft()

            if goal_condition(state):
                return plan

            if len(plan) >= max_depth:
                continue

            for action in self.actions:
                if action.is_applicable(state):
                    new_state = action.apply(state)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, plan + [action]))

        return None  # No plan found
```

### Deliberation Under Uncertainty

Real robots face uncertainty. Markov Decision Processes (MDPs) handle probabilistic outcomes:

```python
class SimpleMDP:
    """Markov Decision Process representation."""

    def __init__(self, states, actions, transition_probs, rewards, gamma=0.9):
        self.states = states
        self.actions = actions
        self.P = transition_probs  # P[s][a][s'] = probability
        self.R = rewards          # R[s][a] = immediate reward
        self.gamma = gamma        # Discount factor

    def value_iteration(self, epsilon=0.001):
        """Compute optimal value function and policy."""
        V = {s: 0 for s in self.states}

        while True:
            delta = 0
            for s in self.states:
                v = V[s]
                # Bellman optimality update
                V[s] = max(
                    self.R[s][a] + self.gamma * sum(
                        self.P[s][a][s_next] * V[s_next]
                        for s_next in self.states
                    )
                    for a in self.actions
                )
                delta = max(delta, abs(v - V[s]))

            if delta < epsilon:
                break

        # Extract policy
        policy = {}
        for s in self.states:
            policy[s] = max(
                self.actions,
                key=lambda a: self.R[s][a] + self.gamma * sum(
                    self.P[s][a][s_next] * V[s_next]
                    for s_next in self.states
                )
            )

        return V, policy
```

---

## 4.4 Hybrid Architectures

### Three-Layer Architecture

Most modern robots use hybrid architectures that combine reactive and deliberative elements:

```
┌─────────────────────────────────────┐
│         DELIBERATIVE LAYER          │
│   (Planning, reasoning, learning)   │
│         Response: seconds           │
├─────────────────────────────────────┤
│          EXECUTIVE LAYER            │
│   (Sequencing, monitoring, adapting)│
│         Response: milliseconds      │
├─────────────────────────────────────┤
│           REACTIVE LAYER            │
│   (Direct sensor-action mappings)   │
│         Response: microseconds      │
└─────────────────────────────────────┘
```

### Implementation Pattern

```python
class HybridArchitecture:
    """Three-layer hybrid cognitive architecture."""

    def __init__(self):
        self.reactive_layer = ReactiveLayer()
        self.executive_layer = ExecutiveLayer()
        self.deliberative_layer = DeliberativeLayer()

        self.current_plan = []
        self.current_task = None

    def update(self, sensor_data, dt):
        """
        Main control loop called at high frequency.
        """
        # Reactive layer always runs (safety)
        if self.reactive_layer.emergency_detected(sensor_data):
            return self.reactive_layer.emergency_action(sensor_data)

        # Executive layer monitors and adapts
        if self.current_task:
            task_status = self.executive_layer.monitor_task(
                self.current_task, sensor_data
            )

            if task_status == 'FAILED':
                # Request replanning
                self.current_plan = []
            elif task_status == 'COMPLETE':
                self.current_task = None

        # Get next task from plan
        if not self.current_task and self.current_plan:
            self.current_task = self.current_plan.pop(0)

        # Execute current task through reactive behaviors
        if self.current_task:
            return self.executive_layer.execute_task(
                self.current_task, sensor_data
            )

        # Default behavior when no plan
        return self.reactive_layer.default_action(sensor_data)

    def set_goal(self, goal):
        """
        Set a high-level goal (called infrequently).
        """
        # Deliberative layer creates a plan
        self.current_plan = self.deliberative_layer.plan(
            self.get_current_state(), goal
        )
```

---

## 4.5 Learning in Cognitive Systems

### Types of Robot Learning

| Type | Learning From | Example |
|------|---------------|---------|
| Supervised | Labeled examples | Object recognition |
| Reinforcement | Trial and error | Walking policies |
| Imitation | Demonstrations | Manipulation tasks |
| Self-supervised | Unlabeled data | World models |

### Reinforcement Learning Basics

```python
class QLearning:
    """Simple Q-learning agent."""

    def __init__(self, states, actions, learning_rate=0.1, discount=0.9, epsilon=0.1):
        self.Q = {s: {a: 0 for a in actions} for s in states}
        self.alpha = learning_rate
        self.gamma = discount
        self.epsilon = epsilon
        self.actions = actions

    def choose_action(self, state):
        """Epsilon-greedy action selection."""
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        else:
            return max(self.actions, key=lambda a: self.Q[state][a])

    def update(self, state, action, reward, next_state):
        """Update Q-value from experience."""
        best_next = max(self.Q[next_state].values())
        td_target = reward + self.gamma * best_next
        td_error = td_target - self.Q[state][action]
        self.Q[state][action] += self.alpha * td_error
```

### Learning from Demonstration

```python
class ImitationLearner:
    """Learn a policy from expert demonstrations."""

    def __init__(self, state_dim, action_dim):
        self.demonstrations = []
        self.policy = None

    def add_demonstration(self, states, actions):
        """Add an expert demonstration."""
        for s, a in zip(states, actions):
            self.demonstrations.append((s, a))

    def train(self):
        """Train policy to match demonstrations (behavioral cloning)."""
        # Extract training data
        X = np.array([d[0] for d in self.demonstrations])
        y = np.array([d[1] for d in self.demonstrations])

        # Fit a simple model (e.g., neural network)
        # This is a placeholder - real implementation would use PyTorch/TensorFlow
        self.policy = self._fit_policy(X, y)

    def get_action(self, state):
        """Get action from learned policy."""
        return self.policy.predict(state)
```

---

## 4.6 Special Considerations for Humanoids

### Humanoid-Specific Challenges

Humanoid robots present unique challenges:

1. **Balance**: Bipedal walking requires constant balance control
2. **Manipulation**: Two arms enable complex bimanual tasks
3. **Social interaction**: Human-like form creates social expectations
4. **High DOF**: 20-50+ joints require efficient control

### Balance and Locomotion

```python
class BipedBalanceController:
    """Simplified balance controller using Zero Moment Point (ZMP)."""

    def __init__(self, robot):
        self.robot = robot
        self.support_polygon = None

    def compute_zmp(self, com_position, com_acceleration, gravity=9.81):
        """
        Compute Zero Moment Point.

        The ZMP is the point where the total reaction force
        produces no moment in the horizontal plane.
        """
        zmp_x = com_position[0] - (com_position[2] / gravity) * com_acceleration[0]
        zmp_y = com_position[1] - (com_position[2] / gravity) * com_acceleration[1]
        return np.array([zmp_x, zmp_y])

    def is_stable(self, zmp):
        """Check if ZMP is within support polygon."""
        return self.point_in_polygon(zmp, self.support_polygon)

    def compute_balance_adjustment(self, current_zmp, target_zmp):
        """Compute torso adjustment to move ZMP toward target."""
        error = target_zmp - current_zmp
        # Simple proportional control for torso lean
        return -0.1 * error
```

### Whole-Body Control

```python
class WholeBodyController:
    """Coordinate multiple tasks across the humanoid body."""

    def __init__(self, robot):
        self.robot = robot
        self.tasks = []

    def add_task(self, task, priority):
        """Add a control task with priority."""
        self.tasks.append((priority, task))
        self.tasks.sort(key=lambda x: x[0])

    def compute_control(self):
        """
        Compute joint commands satisfying all tasks by priority.

        Uses null-space projection to satisfy lower-priority tasks
        without affecting higher-priority ones.
        """
        q_dot = np.zeros(self.robot.num_joints)
        null_space = np.eye(self.robot.num_joints)

        for priority, task in self.tasks:
            # Get task Jacobian and desired velocity
            J = task.get_jacobian()
            x_dot_desired = task.get_desired_velocity()

            # Project into available null space
            J_proj = J @ null_space

            # Compute contribution (pseudoinverse)
            J_pinv = np.linalg.pinv(J_proj)
            q_dot += J_pinv @ (x_dot_desired - J @ q_dot)

            # Update null space
            null_space = null_space @ (np.eye(self.robot.num_joints) - J_pinv @ J_proj)

        return q_dot
```

---

## Hands-On Exercises

### Exercise 4.1: Build a Reactive Controller

1. Create a subsumption-style controller with 3 behaviors
2. Test in a simulated obstacle environment
3. Observe emergent behavior from behavior interactions
4. Add a fourth behavior and document the changes

### Exercise 4.2: Implement a Simple Planner

1. Define a grid world with obstacles
2. Implement A* search for path planning
3. Create an executive layer to follow the planned path
4. Handle cases where the path becomes blocked

### Exercise 4.3: Q-Learning for Navigation

1. Create a simple navigation environment
2. Implement Q-learning to learn a navigation policy
3. Plot the learning curve (reward vs. episodes)
4. Compare learned policy to hand-coded behavior

### Exercise 4.4: Humanoid Balance Simulation

1. Load a humanoid model in PyBullet
2. Implement simplified ZMP-based balance
3. Apply external disturbances and observe recovery
4. Experiment with different control gains

---

## Summary

In this chapter, you learned:

- **Cognitive architectures** integrate perception, planning, and action
- **Reactive architectures** provide fast, robust responses without world models
- **Deliberative architectures** use planning for complex goals
- **Hybrid architectures** combine both approaches in layered systems
- **Learning** enables robots to improve from experience
- **Humanoids** require special attention to balance and coordination

---

## Key Terms

- **Cognitive Architecture**: Overall structure of an intelligent system
- **Subsumption**: Layered reactive architecture
- **Deliberative Planning**: Goal-directed reasoning with world models
- **MDP**: Markov Decision Process for planning under uncertainty
- **Reinforcement Learning**: Learning from trial and error
- **Zero Moment Point (ZMP)**: Balance criterion for bipedal robots

---

## Next Chapter Preview

In Chapter 5, you will learn about **Safety and Ethics in Physical AI**—the critical considerations for deploying robots safely in the real world and the ethical frameworks guiding their development.
