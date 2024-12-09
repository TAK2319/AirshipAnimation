import bpy
import numpy as np
import mathutils


class AirshipAnimator:
    def __init__(self, trajectory_file, trajectory_index=0, airship_name="airshipv5", camera_name="FollowingCamera"):
        self.trajectory_file = trajectory_file
        self.trajectory_index = trajectory_index
        self.airship_name = airship_name
        self.camera_name = camera_name
        self.trajectory = self.load_trajectory()
        self.airship = self.get_airship()
        self.camera = self.get_or_create_camera()
        self.camera_offset = mathutils.Vector((-150, -500, 65))

    def load_trajectory(self):
        """Load trajectory data from a .npy file."""
        trajectories = np.load(self.trajectory_file)
        return trajectories[self.trajectory_index]

    def get_airship(self):
        """Retrieve the airship object."""
        airship = bpy.data.objects.get(self.airship_name)
        if airship is None:
            raise ValueError(f"Object '{self.airship_name}' not found in the scene!")
        return airship

    def get_or_create_camera(self):
        """Get an existing camera or create a new one."""
        camera = bpy.data.objects.get(self.camera_name)
        if camera is None:
            bpy.ops.object.camera_add(
                enter_editmode=False,
                align='VIEW',
                location=(0, 0, 0),
                rotation=(0.921532, 0, 0.460765)
            )
            camera = bpy.context.object
            camera.name = self.camera_name
        return camera

    def add_track_to_constraint(self):
        """Add a 'Track To' constraint to the camera."""
        if not any(constraint.type == 'TRACK_TO' for constraint in self.camera.constraints):
            track_to = self.camera.constraints.new(type='TRACK_TO')
            track_to.target = self.airship
            track_to.track_axis = 'TRACK_NEGATIVE_Z'
            track_to.up_axis = 'UP_Y'

    def set_scene_frame_range(self, start_frame, total_frames):
        """Set the scene's frame range."""
        bpy.context.scene.frame_start = start_frame
        bpy.context.scene.frame_end = start_frame + total_frames

    def create_curve_from_trajectory(self, name="TrajectoryPath"):
        """Create a 3D curve object from trajectory data."""
        curve_data = bpy.data.curves.new(name=name, type='CURVE')
        curve_data.dimensions = '3D'
        polyline = curve_data.splines.new('POLY')
        polyline.points.add(len(self.trajectory) - 1)

        for i, (x, y, z, _, _, _) in enumerate(self.trajectory):
            polyline.points[i].co = (x, y, z, 1)

        curve_object = bpy.data.objects.new(f"{name}Object", curve_data)
        bpy.context.collection.objects.link(curve_object)

    def animate_airship(self, start_frame=0):
        """Animate the airship and camera along the trajectory."""
        total_frames = len(self.trajectory)
        self.set_scene_frame_range(start_frame, total_frames)

        for frame, point in enumerate(self.trajectory, start=start_frame):
            x, y, z = point[:3]
            roll, pitch, _ = point[3:]

            # Compute yaw
            if frame < start_frame + total_frames - 1:
                next_point = self.trajectory[frame - start_frame + 1, :3]
                tangent = next_point - np.array([x, y, z])
            else:
                previous_point = self.trajectory[frame - start_frame - 1, :3]
                tangent = np.array([x, y, z]) - previous_point

            tangent = tangent / np.linalg.norm(tangent)
            yaw = np.arctan2(tangent[1], tangent[0])

            # Apply transformations to the airship
            self.airship.location = (x, y, z)
            self.airship.rotation_euler = mathutils.Euler((roll, pitch, yaw + np.pi), 'XYZ')
            self.airship.keyframe_insert(data_path="location", frame=frame)
            self.airship.keyframe_insert(data_path="rotation_euler", frame=frame)

            # Apply transformations to the camera
            self.camera.location = mathutils.Vector((x, y, z)) + self.camera_offset
            self.camera.keyframe_insert(data_path="location", frame=frame)

    def run(self):
        """Run the animation process."""
        self.create_curve_from_trajectory()
        self.add_track_to_constraint()
        self.animate_airship()


# Main Execution
if __name__ == "__main__":
    trajectory_file = "/Users/mydaddy/Desktop/Blender Files/trajectories.npy"
    animator = AirshipAnimator(trajectory_file=trajectory_file, trajectory_index=4)
    animator.run()