## Airship Animator for Blender

This Python script animates an airship in Blender based on a 3D trajectory dataset. It utilizes object-oriented programming principles for modularity and reusability, enabling smooth animation and camera tracking along the given path. For convenience procedural and function programming files are also included.

## Features

- Load 3D trajectory data from a `.npy` file.
- Animate an airship's position and orientation based on roll, pitch, and yaw data.
- Create a visual trajectory curve in the Blender scene.
- Add a camera with a `Track To` constraint to follow the airship.
- Customizable camera offset and trajectory selection.

## Requirements

- **Blender** (with Python scripting capabilities)
- **NumPy** (for handling trajectory data)

## Installation

1. Ensure you have NumPy installed:
   ```bash
   pip install numpy
   ```

2. Open Blender, then navigate to the **Scripting** workspace.

3. Load the script file in Blender's text editor.

## Usage

### 1. Prepare the Input Data
- Save your trajectory data as a `.npy` file. Each trajectory should be a 2D array with the shape `(N, 6)` where:
  - The first three columns represent `x`, `y`, and `z` coordinates.
  - The last three columns represent roll, pitch, and yaw angles.

### 2. Update Script Parameters
Modify the following parameters in the script:
- `trajectory_file`: Path to your `.npy` file.
- `trajectory_index`: Index of the trajectory to animate (default is `4`).
- `airship_name`: Name of the airship object in your Blender scene.
- `camera_name`: Name of the camera to follow the airship.

### 3. Run the Script
- Execute the script in Blender's **Scripting** workspace.
- The airship and camera will animate along the selected trajectory.

## Example Output

- An airship following a smooth path with a camera tracking its movement.
- A 3D curve representing the trajectory.

## Code Overview

The script is organized into a single class: `AirshipAnimator`.

### Key Methods
- `__init__`: Initialize trajectory, airship, and camera parameters.
- `load_trajectory`: Load trajectory data from a file.
- `get_airship` / `get_or_create_camera`: Retrieve or create scene objects.
- `add_track_to_constraint`: Add a `Track To` constraint to the camera.
- `create_curve_from_trajectory`: Generate a 3D curve for the trajectory.
- `animate_airship`: Animate the airship and camera.
- `run`: Orchestrate the animation workflow.

### Example Snippet
```python
trajectory_file = "/path/to/trajectories.npy"
animator = AirshipAnimator(trajectory_file=trajectory_file, trajectory_index=4)
animator.run()
```

