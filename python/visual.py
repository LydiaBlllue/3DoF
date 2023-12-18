import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the figure for plotting
#4 graphs, accelerometer, gyroscope, magnetometer, and euler angles
fig, ax = plt.subplots(4)




def update(frame):

    

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
