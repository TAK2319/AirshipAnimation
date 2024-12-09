"""This Code is just to inspect the data and visualize a potential trajectory for the aircraft in 3D (x,y,z)"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the trajectory data
trajectory_file = "/Users/mydaddy/Desktop/Blender Files/trajectories.npy"  # Update this path/filename with yours if necessary
trajectories = np.load(trajectory_file)
print(trajectories)

# Select the first trajectory (shape: (1000, 6)) for example
trajectory = trajectories[4]

# Extract x, y, z positions
x = trajectory[:, 0]
y = trajectory[:, 1]
z = trajectory[:, 2]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the path
ax.plot(x, y, z, label='Trajectory Path', color='b')

# Labels and title
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')
ax.set_title('3D Path of the Trajectory')

# Show the plot
plt.legend()
plt.show()
