---
sidebar_position: 1
title: Troubleshooting
description: Solutions to common issues when working through the Physical AI book
keywords: [troubleshooting, help, errors, pybullet, installation]
---

# Troubleshooting

This guide covers common issues you might encounter while working through the book.

## Installation Issues

### PyBullet Won't Install

#### Windows

**Error**: `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution**:
1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Select "Desktop development with C++" workload
3. Retry: `pip install pybullet`

Alternative (pre-built wheel):
```bash
pip install pybullet --no-cache-dir
```

#### Linux (Ubuntu/Debian)

**Error**: `Python.h: No such file or directory`

**Solution**:
```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
pip install pybullet
```

#### Graphics Issues

**Error**: `cannot open display` or `GLFW error`

**Solution for WSL2**:
```bash
# Install X server on Windows (VcXsrv or Xming)
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
```

**Headless Mode** (no GUI):
```python
import pybullet as p
# Use DIRECT mode instead of GUI
physics_client = p.connect(p.DIRECT)
```

---

### NumPy Compatibility Issues

**Error**: `numpy.core.multiarray failed to import`

**Solution**:
```bash
pip uninstall numpy
pip install numpy==1.24.0
```

---

### Python Virtual Environment Issues

**Error**: `ModuleNotFoundError` after installation

**Solution**: Ensure you activated the virtual environment:

```bash
# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Verify correct Python
which python
pip list
```

---

## Code Example Issues

### Simulation Window Doesn't Open

**Possible causes**:
1. Using headless mode (`p.DIRECT` instead of `p.GUI`)
2. Graphics driver issues
3. Running on remote server without display

**Solutions**:

1. Change connection mode:
```python
# For visualization
physics_client = p.connect(p.GUI)

# For headless (testing/CI)
physics_client = p.connect(p.DIRECT)
```

2. Update graphics drivers

3. For remote servers, use X forwarding:
```bash
ssh -X user@server
```

---

### Robot Model Won't Load

**Error**: `Cannot load URDF file`

**Solutions**:

1. Set the search path:
```python
import pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())
```

2. Use absolute path:
```python
import os
urdf_path = os.path.join(os.path.dirname(__file__), "robot.urdf")
robot_id = p.loadURDF(urdf_path)
```

---

### Simulation Runs Too Fast/Slow

**Problem**: Physics doesn't look realistic

**Solution**: Use real-time stepping:
```python
import time

# Real-time simulation
p.setRealTimeSimulation(1)

# Or manual stepping at 240Hz
while True:
    p.stepSimulation()
    time.sleep(1./240.)
```

---

## Development Environment Issues

### Docusaurus Build Fails

**Error**: `Module not found` or build errors

**Solutions**:

1. Clear cache and reinstall:
```bash
rm -rf node_modules .docusaurus
npm install
npm run build
```

2. Check Node.js version (requires 18+):
```bash
node --version
```

3. Increase memory limit:
```bash
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

---

### Hot Reload Not Working

**Problem**: Changes don't appear in browser

**Solutions**:

1. Check for syntax errors in MDX files
2. Restart the dev server:
```bash
# Ctrl+C to stop
npm run start
```
3. Clear browser cache (Ctrl+Shift+R)
4. Check for JavaScript errors in browser console

---

## Chapter-Specific Issues

### Chapter 2: Sensor Data Noise

**Problem**: Sensor readings are too noisy

**Solution**: Apply filtering:
```python
# Simple moving average
def moving_average(data, window=5):
    return sum(data[-window:]) / min(len(data), window)
```

### Chapter 3: Inverse Kinematics Fails

**Problem**: IK returns `None` or wrong solution

**Possible causes**:
1. Target is outside reachable workspace
2. Singularity condition
3. Numerical precision issues

**Solutions**:
```python
# Check reachability
distance = np.linalg.norm(target)
if distance > L1 + L2:
    print("Target unreachable - outside workspace")

# Try multiple initial guesses
for _ in range(10):
    initial_guess = np.random.uniform(-np.pi, np.pi, n_joints)
    solution = solve_ik(target, initial_guess)
    if solution is not None:
        break
```

### Chapter 4: Balance Controller Unstable

**Problem**: Simulated robot falls over

**Solutions**:
1. Reduce time step for stability:
```python
p.setTimeStep(1./480.)  # 480Hz instead of 240Hz
```

2. Tune PID gains (start small):
```python
Kp = 0.1  # Start small
Ki = 0.0  # Often not needed
Kd = 0.01
```

3. Check ZMP calculation:
```python
# Verify ZMP is within support polygon
assert is_inside_polygon(zmp, support_polygon)
```

---

## Getting More Help

If your issue isn't covered here:

1. **Search existing issues**: [GitHub Issues](https://github.com/physical-ai-book/physical-ai-book/issues)
2. **Ask a question**: [GitHub Discussions](https://github.com/physical-ai-book/physical-ai-book/discussions)
3. **Report a bug**: [New Issue](https://github.com/physical-ai-book/physical-ai-book/issues/new)

When reporting issues, please include:
- Operating system and version
- Python version
- PyBullet version
- Full error message and stack trace
- Code that reproduces the issue
