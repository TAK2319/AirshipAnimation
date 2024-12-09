"""The Code below is the base for the functional and object oriented solutions and corrects the yaw for 
making the airship follow the tangent of the trajectory"""

import bpy
import numpy as np
import mathutils

# Load the trajectory data
trajectory_file = "/Users/mydaddy/Desktop/Blender Files/trajectories.npy"  # Update this path as needed necessary
trajectories = np.load(trajectory_file)

# Select the trajectory (assumes shape: (1000, 6))
trajectory = trajectories[4]

# Get the airship object
airship = bpy.data.objects.get("airshipv5")
if airship is None:
   raise ValueError("Object 'airshipv5' not found in the scene!")

# Add a camera if it doesn't already exist
camera_name = "FollowingCamera"
camera = bpy.data.objects.get(camera_name)
if camera is None:
   bpy.ops.object.camera_add(
       enter_editmode=False, 
       align='VIEW', 
       location=(0, 0, 0), 
       rotation=(0.921532, 0, 0.460765), 
       scale=(1, 1, 1)
   )
   camera = bpy.context.object
   camera.name = camera_name

# Add a "Track To" constraint to keep the camera pointed at the airship
if not any(constraint.type == 'TRACK_TO' for constraint in camera.constraints):
   track_to = camera.constraints.new(type='TRACK_TO')
   track_to.target = airship
   track_to.track_axis = 'TRACK_NEGATIVE_Z'
   track_to.up_axis = 'UP_Y'

# Set the initial frame range
start_frame = 0
total_frames = len(trajectory)
bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end = start_frame + total_frames

# Define camera offset relative to the airship
camera_offset = mathutils.Vector((-150, -500, 65))  # 10 units forward, 20 right, 20 above

# Animate the airship and camera
for frame, point in enumerate(trajectory, start=start_frame):
   # Set the airship's location
   x, y, z = point[:3]
   airship.location = (x, y, z)

   # Extract roll and pitch from the trajectory
   roll, pitch, _ = point[3:]

   # Compute tangent vector for yaw calculation
   if frame < start_frame + total_frames - 1:
       next_point = trajectory[frame - start_frame + 1, :3]
       tangent = next_point - np.array([x, y, z])
   else:
       previous_point = trajectory[frame - start_frame - 1, :3]
       tangent = np.array([x, y, z]) - previous_point

   tangent = tangent / np.linalg.norm(tangent)  # Normalize the tangent vector
   yaw = np.arctan2(tangent[1], tangent[0])  # Calculate yaw from tangent vector

   # Apply roll, pitch, yaw to the airship
   airship.rotation_euler = mathutils.Euler(
       (roll, pitch, yaw + np.pi), 'XYZ'
   )
   airship.keyframe_insert(data_path="location", frame=frame)
   airship.keyframe_insert(data_path="rotation_euler", frame=frame)

   # Set the camera position relative to the airship
   camera.location = mathutils.Vector((x, y, z)) + camera_offset
   camera.keyframe_insert(data_path="location", frame=frame)
   
"Below is the Code for the 'for loop' before yaw correction based on the path tangent"

#for frame, point in enumerate(trajectory, start=start_frame):
#    # Set the object's location (first three values are x, y, z)
#    x, y, z = point[:3]
#    obj.location = (x, y, z)
#    
#    # Set the object's rotation (last three values are Euler angles: roll, pitch, yaw)
#    roll, pitch, yaw = point[3:]
#    # Linearly interpolate yaw adjustment
#    interpolation_factor = (total_frames - (frame - start_frame)) / total_frames  # Progressively decreases from 1 to 0
#    yaw_adjustment = np.pi * interpolation_factor + (np.pi * 3 / 5) * (1 - interpolation_factor)

#    # Apply the calculated yaw adjustment
#    obj.rotation_euler = (
#        roll,
#        pitch,
#        yaw + yaw_adjustment
#    )

#    # Insert keyframes for location and rotation
#    obj.keyframe_insert(data_path="location", frame=frame)
#    obj.keyframe_insert(data_path="rotation_euler", frame=frame)
