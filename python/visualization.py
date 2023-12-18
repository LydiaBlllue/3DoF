
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("orientation_data.csv")


#plot three orientations in three subplots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))

# Plot each orientation on its own subplot
axes[0].plot(data["Roll"])
axes[1].plot(data["Pitch"])
axes[2].plot(data["Yaw"])

# Label axes
axes[0].set_title("Roll")
axes[1].set_title("Pitch")
axes[2].set_title("Yaw")

# Display plot
plt.show()

'''
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# Assuming the CSV has columns named 'Roll', 'Pitch', and 'Yaw'
roll = data['Roll']
pitch = data['Pitch']
yaw = data['Yaw']

# Create a figure for 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a cube representation for the orientation
# Define the size of the cube
cube_dim = 0.5
# Define the corners of the cube
cube = np.array([[-cube_dim, -cube_dim, -cube_dim],
                 [cube_dim, -cube_dim, -cube_dim],
                 [cube_dim, cube_dim, -cube_dim],
                 [-cube_dim, cube_dim, -cube_dim],
                 [-cube_dim, -cube_dim, cube_dim],
                 [cube_dim, -cube_dim, cube_dim],
                 [cube_dim, cube_dim, cube_dim],
                 [-cube_dim, cube_dim, cube_dim]])

# Define the edges of the cube
edges = [[cube[i], cube[j]] for i in range(len(cube)) for j in range(i+1, len(cube)) if np.sum(np.abs(cube[i]-cube[j])) == cube_dim*2]

# Function to rotate the cube
def rotate_cube(cube, roll, pitch, yaw):
    # Convert angles from degrees to radians for computation
    roll = np.radians(roll)
    pitch = np.radians(pitch)
    yaw = np.radians(yaw)
    
    # Rotation matrices around the X, Y, and Z axis
    RX = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])
    
    RY = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])
    
    RZ = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])
    
    # Combined rotation matrix
    R = np.dot(RZ, np.dot(RY, RX))
    
    # Apply the rotation to the cube
    rotated_cube = np.dot(cube, R)
    return rotated_cube

# Plot the cube
def plot_cube(ax, cube, color='b'):
    for edge in edges:
        ax.plot3D(*zip(*edge), color=color)

# Initialize the cube plot
plot_cube(ax, cube, color='r')

# Display the first orientation (assuming the CSV is sorted by time and the first row is the initial orientation)
rotated_cube = rotate_cube(cube, roll[0], pitch[0], yaw[0])
plot_cube(ax, rotated_cube, color='g')

# Set the labels and title
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('3D Cube Orientation Visualization')

# Show the plot
plt.show()




'''