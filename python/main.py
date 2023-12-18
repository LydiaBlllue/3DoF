import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Serial setup
ser = serial.Serial('/dev/cu.usbmodem14401', 115200, timeout=1)
time.sleep(2)

# Plot setup
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)
fig.suptitle('IMU Data Visualization')
ax1.set_ylabel('Acceleration (m/s^2)')
ax2.set_ylabel('Gyroscope (rad/s)')
ax3.set_ylabel('Magnetometer (uT)')
ax4.set_ylabel('Orientation (degrees)')
ax4.set_xlabel('Time (ms)')

time_data = []
accel_data = []
gyro_data = []
mag_data = []
orientation_data = []

def read_save_data():
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            #print("Raw data:", line)  # Print raw data for debugging
            data = line.split(',')

            if len(data) >= 13:  # Adjust this based on the actual number of expected data points
            
                #save the data to lists
                time_data.append(int(data[0]))
                accel_data.append((float(data[1]), float(data[2]), float(data[3])))
                gyro_data.append((float(data[4]), float(data[5]), float(data[6])))
                mag_data.append((float(data[7]), float(data[8]), float(data[9])))
                orientation_data.append((float(data[10]), float(data[11]), float(data[12])))

                return {
                    'timestamp': int(data[0]),
                    'accel': {'x': float(data[1]), 'y': float(data[2]), 'z': float(data[3])},
                    'gyro': {'x': float(data[4]), 'y': float(data[5]), 'z': float(data[6])},
                    'mag': {'x': float(data[7]), 'y': float(data[8]), 'z': float(data[9])},
                    'orientation': {'x': float(data[10]), 'y': float(data[11]), 'z': float(data[12])}
                }

            else:
                return None
    
    except Exception as e:
        print("Error parsing data:", e)
def update(frame):

    parsed_data = read_save_data()
    if parsed_data:
        
        # only plot the latest 100 data points 
        range = 100

        # Update data
        time_slice = time_data[-range:]
        accel_x = [x[0] for x in accel_data[-range:]]
        accel_y = [y[1] for y in accel_data[-range:]]
        accel_z = [z[2] for z in accel_data[-range:]]

        gyro_x = [x[0] for x in gyro_data[-range:]]
        gyro_y = [y[1] for y in gyro_data[-range:]]
        gyro_z = [z[2] for z in gyro_data[-range:]]

        mag_x = [x[0] for x in mag_data[-range:]]
        mag_y = [y[1] for y in mag_data[-range:]]
        mag_z = [z[2] for z in mag_data[-range:]]

        orientation_x = [x[0] for x in orientation_data[-range:]]
        orientation_y = [y[1] for y in orientation_data[-range:]]
        orientation_z = [z[2] for z in orientation_data[-range:]]

        # Update plots
        # Check if lines exist, update data if they do, else create new lines
        if hasattr(update, 'accel_lines'):
            update.accel_lines[0].set_data(time_slice, accel_x)
            update.accel_lines[1].set_data(time_slice, accel_y)
            update.accel_lines[2].set_data(time_slice, accel_z)
            # Update for gyro, mag, and orientation similarly
        else:
            update.accel_lines = [ax1.plot(time_slice, accel_x, label='X')[0],
                                  ax1.plot(time_slice, accel_y, label='Y')[0],
                                  ax1.plot(time_slice, accel_z, label='Z')[0]]
        
        ax1.relim()
        ax1.autoscale_view()
        ax1.legend()

        #gyro
        if hasattr(update, 'gyro_lines'):
            update.gyro_lines[0].set_data(time_slice, gyro_x)
            update.gyro_lines[1].set_data(time_slice, gyro_y)
            update.gyro_lines[2].set_data(time_slice, gyro_z)
        else:
            update.gyro_lines = [ax2.plot(time_slice, gyro_x, label='X')[0],
                                  ax2.plot(time_slice, gyro_y, label='Y')[0],
                                  ax2.plot(time_slice, gyro_z, label='Z')[0]]
            
        ax2.relim()
        ax2.autoscale_view()
        ax2.legend()

        #mag
        if hasattr(update, 'mag_lines'):
            update.mag_lines[0].set_data(time_slice, mag_x)
            update.mag_lines[1].set_data(time_slice, mag_y)
            update.mag_lines[2].set_data(time_slice, mag_z)
        else:
            update.mag_lines = [ax3.plot(time_slice, mag_x, label='X')[0],
                                  ax3.plot(time_slice, mag_y, label='Y')[0],
                                  ax3.plot(time_slice, mag_z, label='Z')[0]]
            
        ax3.relim()
        ax3.autoscale_view()
        ax3.legend()

        #orientation

        if hasattr(update, 'orientation_lines'):
            update.orientation_lines[0].set_data(time_slice, orientation_x)
            update.orientation_lines[1].set_data(time_slice, orientation_y)
            update.orientation_lines[2].set_data(time_slice, orientation_z)
        else:
            update.orientation_lines = [ax4.plot(time_slice, orientation_x, label='X')[0],
                                  ax4.plot(time_slice, orientation_y, label='Y')[0],
                                  ax4.plot(time_slice, orientation_z, label='Z')[0]]
            
        ax4.relim()
        ax4.autoscale_view()
        ax4.legend()

    return update.accel_lines + update.gyro_lines + update.mag_lines + update.orientation_lines





# Create animation
ani = animation.FuncAnimation(fig, update, interval=100)

# Show plot
plt.show()

#write the data to a csv file named imu_data.csv
with open('imu_data.csv', 'w') as f:
    f.write('timestamp,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,mag_x,mag_y,mag_z,orientation_x,orientation_y,orientation_z\n')
    for i in range(len(time_data)):
        f.write((time_data[i],
                            accel_data[i][0], accel_data[i][1], accel_data[i][2],
                            gyro_data[i][0], gyro_data[i][1], gyro_data[i][2],
                            mag_data[i][0], mag_data[i][1], mag_data[i][2],
                            orientation_data[i][0], orientation_data[i][1], orientation_data[i][2]
                            ))
        f.write('\n')

# Close serial port



        


