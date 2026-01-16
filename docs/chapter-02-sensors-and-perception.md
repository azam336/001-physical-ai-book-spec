---
sidebar_position: 2
title: "Chapter 2: Sensors and Perception"
description: "How physical AI systems perceive the world through sensors and process raw data into meaningful information"
keywords: [sensors, perception, computer vision, lidar, sensor fusion, filtering]
---

# Chapter 2: Sensors and Perception

**Estimated Time**: 4-5 hours
**Prerequisites**: Chapter 1 completion, basic linear algebra concepts (vectors, matrices)

## Learning Outcomes

By the end of this chapter, you will be able to:

- Identify common sensor types used in physical AI systems and their characteristics
- Explain how raw sensor data is transformed into actionable information
- Implement basic perception pipelines for different sensor modalities
- Apply filtering and fusion techniques to handle sensor noise and uncertainty

---

## 2.1 Introduction to Sensors

### Why Sensors Matter

Sensors are the eyes, ears, and touch of an Embodied AI system. Without accurate perception, no amount of sophisticated planning can produce good behavior. The quality of a robot's decisions is fundamentally limited by the quality of its sensory information.

### The Sensing Challenge

Real-world sensors present several challenges:

- **Noise**: All sensors produce imperfect measurements
- **Latency**: Time delay between physical event and data availability
- **Calibration**: Sensors require careful setup to produce accurate readings
- **Environmental sensitivity**: Temperature, lighting, and other factors affect performance

---

## 2.2 Sensor Types and Characteristics

### Vision Sensors (Cameras)

Cameras capture rich visual information about the environment.

**Types**:
- **RGB cameras**: Standard color images
- **Depth cameras**: Distance to each pixel (RGB-D)
- **Stereo cameras**: Two cameras for depth estimation
- **Event cameras**: Detect changes in brightness asynchronously

**Characteristics**:

| Property | Typical Value |
|----------|---------------|
| Resolution | 640x480 to 4K |
| Frame rate | 30-120 fps |
| Field of view | 60-180 degrees |
| Range | Limited by lighting |

**Strengths**: Rich information, passive sensing, relatively inexpensive

**Weaknesses**: Affected by lighting, computationally intensive, depth requires additional processing

### LIDAR (Light Detection and Ranging)

LIDAR uses laser pulses to measure distances with high precision.

**How it works**:
1. Emit laser pulse
2. Measure time for reflection to return
3. Calculate distance using speed of light
4. Rotate or scan to build 3D point cloud

**Characteristics**:

| Property | Typical Value |
|----------|---------------|
| Points per second | 300K - 2M |
| Range | 100-300 meters |
| Angular resolution | 0.1-0.4 degrees |
| Accuracy | 2-5 cm |

**Strengths**: Precise distance measurements, works in darkness, direct 3D data

**Weaknesses**: Expensive, affected by rain/fog, sparse data compared to cameras

### Inertial Measurement Units (IMUs)

IMUs measure acceleration and rotation rates.

**Components**:
- **Accelerometer**: Measures linear acceleration (3 axes)
- **Gyroscope**: Measures angular velocity (3 axes)
- **Magnetometer**: Measures magnetic field (optional, for heading)

**Characteristics**:

| Property | Typical Value |
|----------|---------------|
| Update rate | 100-1000 Hz |
| Accelerometer range | +/- 16g |
| Gyroscope range | +/- 2000 deg/s |

**Strengths**: Fast update rate, no external dependencies, compact

**Weaknesses**: Drift over time, requires calibration, affected by vibration

### Touch and Force Sensors

Touch sensors provide information about physical contact.

**Types**:
- **Tactile arrays**: Grid of pressure sensors
- **Force/torque sensors**: 6-axis force measurement
- **Whisker sensors**: Detect proximity through touch

**Applications**: Grasping, manipulation, collision detection

### Proprioceptive Sensors

Proprioception refers to sensing the robot's own body state.

**Types**:
- **Joint encoders**: Measure joint angles
- **Motor current sensors**: Indicate applied torque
- **Strain gauges**: Measure structural deformation

---

## 2.3 From Raw Data to Perception

### The Perception Pipeline

```
Raw Sensor Data
      │
      ▼
┌─────────────┐
│ Calibration │ ◄── Remove systematic errors
└─────────────┘
      │
      ▼
┌─────────────┐
│  Filtering  │ ◄── Reduce noise
└─────────────┘
      │
      ▼
┌─────────────┐
│  Features   │ ◄── Extract meaningful patterns
└─────────────┘
      │
      ▼
┌─────────────┐
│   Fusion    │ ◄── Combine multiple sources
└─────────────┘
      │
      ▼
World Model
```

### Calibration

Calibration corrects systematic errors in sensor measurements.

**Camera calibration** determines:
- Focal length and optical center (intrinsic parameters)
- Camera position and orientation (extrinsic parameters)
- Lens distortion coefficients

**IMU calibration** corrects for:
- Bias: Constant offset in measurements
- Scale factor: Linear scaling error
- Misalignment: Sensor axes not perfectly orthogonal

### Noise Filtering

#### Moving Average Filter

Smooths data by averaging recent measurements:

```python
import numpy as np

def moving_average(data, window_size):
    """Apply moving average filter to sensor data."""
    filtered = np.zeros(len(data))
    for i in range(len(data)):
        start = max(0, i - window_size + 1)
        filtered[i] = np.mean(data[start:i+1])
    return filtered
```

#### Kalman Filter

The Kalman filter optimally estimates state from noisy measurements:

```python
class SimpleKalmanFilter:
    """1D Kalman filter for position estimation."""

    def __init__(self, process_noise, measurement_noise):
        self.Q = process_noise      # Process noise variance
        self.R = measurement_noise  # Measurement noise variance
        self.x = 0                  # State estimate
        self.P = 1                  # Estimate uncertainty

    def update(self, measurement):
        # Prediction step
        # (For stationary target, prediction = previous estimate)

        # Update step
        K = self.P / (self.P + self.R)  # Kalman gain
        self.x = self.x + K * (measurement - self.x)
        self.P = (1 - K) * self.P + self.Q

        return self.x
```

---

## 2.4 Computer Vision Fundamentals

### Image Representation

Digital images are stored as 2D or 3D arrays:

- **Grayscale**: 2D array, values 0-255
- **RGB color**: 3D array (height x width x 3 channels)
- **Depth images**: 2D array, values represent distance

### Basic Image Processing

```python
import numpy as np

def threshold_image(image, threshold):
    """Convert grayscale image to binary."""
    return (image > threshold).astype(np.uint8) * 255

def find_edges(image):
    """Simple edge detection using gradient."""
    # Sobel kernels for x and y gradients
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
    kernel_y = np.array([[-1, -2, -1],
                         [ 0,  0,  0],
                         [ 1,  2,  1]])

    # Apply convolution (simplified)
    gradient_x = convolve2d(image, kernel_x)
    gradient_y = convolve2d(image, kernel_y)

    # Magnitude of gradient
    edges = np.sqrt(gradient_x**2 + gradient_y**2)
    return edges
```

### Object Detection Concepts

Object detection answers: "What objects are in this image, and where?"

**Traditional approaches**:
1. Feature extraction (corners, edges, textures)
2. Feature matching against templates
3. Classification and localization

**Modern deep learning approaches**:
1. Convolutional neural networks (CNNs)
2. Region-based methods (R-CNN family)
3. Single-shot detectors (YOLO, SSD)

---

## 2.5 Point Cloud Processing

### Understanding Point Clouds

LIDAR and depth cameras produce point clouds: sets of 3D points representing surfaces in the environment.

```python
# Point cloud: N x 3 array (x, y, z coordinates)
point_cloud = np.array([
    [1.0, 2.0, 0.5],
    [1.1, 2.1, 0.6],
    [3.0, 1.0, 1.2],
    # ... thousands more points
])
```

### Ground Plane Detection

Separating ground from obstacles is essential for navigation:

```python
def simple_ground_filter(points, height_threshold=0.1):
    """Separate ground points from obstacle points."""
    # Find lowest points (likely ground)
    min_z = np.min(points[:, 2])

    # Points near minimum height are ground
    ground_mask = points[:, 2] < (min_z + height_threshold)

    ground_points = points[ground_mask]
    obstacle_points = points[~ground_mask]

    return ground_points, obstacle_points
```

### Clustering

Grouping nearby points into objects:

```python
def euclidean_clustering(points, distance_threshold):
    """Cluster points that are within distance_threshold of each other."""
    clusters = []
    remaining = set(range(len(points)))

    while remaining:
        # Start new cluster with arbitrary point
        seed = remaining.pop()
        cluster = [seed]
        queue = [seed]

        while queue:
            current = queue.pop(0)
            for i in list(remaining):
                dist = np.linalg.norm(points[current] - points[i])
                if dist < distance_threshold:
                    remaining.remove(i)
                    cluster.append(i)
                    queue.append(i)

        clusters.append(cluster)

    return clusters
```

---

## 2.6 Sensor Fusion

### Why Fuse Sensors?

No single sensor is perfect. Sensor fusion combines multiple sources to achieve:

- **Complementary information**: Different sensors perceive different things
- **Redundancy**: If one sensor fails, others continue working
- **Improved accuracy**: Multiple measurements reduce uncertainty

### Fusion Strategies

**Early fusion**: Combine raw data before processing
- Example: Merge LIDAR points with camera colors

**Late fusion**: Combine high-level interpretations
- Example: Merge object detections from camera and LIDAR

**Probabilistic fusion**: Use uncertainty to weight contributions
- Example: Kalman filter combining IMU and GPS

### Example: Camera-LIDAR Fusion

```python
def project_lidar_to_camera(lidar_points, camera_matrix, transform):
    """Project 3D LIDAR points onto 2D camera image."""
    # Transform LIDAR points to camera coordinate frame
    points_camera = transform @ lidar_points

    # Project to image plane
    points_2d = camera_matrix @ points_camera[:3, :]

    # Normalize by depth
    pixels = points_2d[:2, :] / points_2d[2, :]

    return pixels
```

---

## Hands-On Exercises

### Exercise 2.1: Implement a Kalman Filter

Using the SimpleKalmanFilter class above:

1. Generate synthetic noisy position measurements
2. Apply the Kalman filter
3. Plot the true position, noisy measurements, and filtered estimate
4. Experiment with different process and measurement noise values

### Exercise 2.2: Point Cloud Ground Segmentation

1. Load a sample point cloud (provided in course materials)
2. Implement ground plane detection
3. Visualize ground points in one color and obstacle points in another
4. Handle sloped terrain (hint: use RANSAC to fit a plane)

### Exercise 2.3: Simple Object Detection

1. Set up a PyBullet simulation with multiple objects
2. Capture an RGB image from a simulated camera
3. Apply color thresholding to detect objects of a specific color
4. Draw bounding boxes around detected objects

---

## Summary

In this chapter, you learned:

- **Sensors** are the foundation of perception in Embodied AI
- Different sensor types (cameras, LIDAR, IMUs, touch) have distinct strengths and weaknesses
- **Calibration** and **filtering** are essential for accurate measurements
- **Computer vision** transforms images into semantic understanding
- **Point cloud processing** handles 3D data from LIDAR and depth sensors
- **Sensor fusion** combines multiple sources for robust perception

---

## Key Terms

- **Sensor fusion**: Combining data from multiple sensors
- **Kalman filter**: Optimal estimator for linear systems with Gaussian noise
- **Point cloud**: Set of 3D points representing surfaces
- **Calibration**: Correcting systematic sensor errors
- **IMU**: Inertial Measurement Unit (accelerometer + gyroscope)

---

## Next Chapter Preview

In Chapter 3, you will learn about **Kinematics and Actuation**—how robots move and interact with the physical world through motors and control systems.
