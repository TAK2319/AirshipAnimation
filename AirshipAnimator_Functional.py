import bpy
import numpy as np
import mathutils


def load_trajectory(file_path, index=0):
    """Load trajectory data from a .npy file."""
    trajectories = np.load(file_path)
    return trajectories[index]


def create_curve_from_trajectory(trajectory, name="TrajectoryPath"):
    """Create a 3D curve object from trajectory data."""
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    polyline = curve_data.splines.new('POLY')
    polyline.points.add(len(trajectory) - 1)

    for i, (x, y, z, _, _, _) in enumerate(trajectory):
        polyline.points[i].co = (x, y, z, 1)

    curve_object = bpy.data.objects.new(f"{name}Object", curve_data)
    bpy.context.collection.objects.link(curve_object)
    return curve_object


def get_or_create_camera(name="FollowingCamera", location=(0, 0, 0), rotation=(0.921532, 0, 0.460765)):
    """Get an existing camera or create a new one."""
    camera = bpy.data.objects.get(name)
    if camera is None:
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=location, rotation=rotation)
        camera = bpy.context.object
        camera.name = name
    return camera


def add_track_to_constraint(camera, target, track_axis='TRACK_NEGATIVE_Z', up_axis='UP_Y'):
    """Add a 'Track To' constraint to a camera."""
    if not any(constraint.type == 'TRACK_TO' for constraint in camera.constraints):
        track_to = camera.constraints.new(type='TRACK_TO')
        track_to.target = target
        track_to.track_axis = track_axis
        track_to.up_axis = up_axis


def set_scene_frame_range(start_frame, total_frames):
    """Set the scene's frame range."""
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = start_frame + total_frames


def animate_object_along_trajectory(obj, trajectory, start_frame, camera=None, camera_offset=None):
    """Animate an object along the given trajectory."""
    total_frames = len(trajectory)

    for frame, point in enumerate(trajectory, start=start_frame):
        x, y, z = point[:3]
        roll, pitch, _ = point[3:]

        # Compute yaw
        if frame < start_frame + total_frames - 1:
            next_point = trajectory[frame - start_frame + 1, :3]
            tangent = next_point - np.array([x, y, z])
        else:
            previous_point = trajectory[frame - start_frame - 1, :3]
            tangent = np.array([x, y, z]) - previous_point

        tangent = tangent / np.linalg.norm(tangent)
        yaw = np.arctan2(tangent[1], tangent[0])

        # Apply transformations
        obj.location = (x, y, z)
        obj.rotation_euler = mathutils.Euler((roll, pitch, yaw + np.pi), 'XYZ')
        obj.keyframe_insert(data_path="location", frame=frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)

        if camera and camera_offset:
            camera.location = mathutils.Vector((x, y, z)) + camera_offset
            camera.keyframe_insert(data_path="location", frame=frame)


def main():
    trajectory_file = "/Users/mydaddy/Desktop/Blender Files/trajectories.npy"
    trajectory_index = 4 #Change the trajectory number here: 0-9, Default is zero 

    # Load trajectory and create a curve
    trajectory = load_trajectory(trajectory_file, index=trajectory_index)
    create_curve_from_trajectory(trajectory)

    # Get or create airship object
    airship = bpy.data.objects.get("airshipv5")
    if airship is None:
        raise ValueError("Object 'airshipv5' not found in the scene!")

    # Get or create camera and add constraints
    camera = get_or_create_camera()
    add_track_to_constraint(camera, airship)

    # Set frame range
    start_frame = 0
    total_frames = len(trajectory)
    set_scene_frame_range(start_frame, total_frames)

    # Define camera offset and animate objects
    camera_offset = mathutils.Vector((-150, -500, 65)) 
    animate_object_along_trajectory(airship, trajectory, start_frame, camera, camera_offset)


# Run the main function
main()