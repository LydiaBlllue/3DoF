import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import queue

huffmanCode = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    ',': '1010',
    '.': '1011',
    '<': '1100',
    '>': '1110',
    '-': '1111'}

def huffman_decode(encodedStr, huffmanCode):
    # Invert the huffmanCode dictionary to create a decoding dictionary
    # This converts { '0': '0000', '1': '0001', ...} to {'0000': '0', '0001': '1', ...}
    decodeDict = {v: k for k, v in huffmanCode.items()}
    
    # Initialize an empty string to hold the decoded characters
    decodedStr = ''
    
    # Process the encoded string in 4-bit chunks since all codes are 4 bits long
    for i in range(0, len(encodedStr), 4):
        # Extract a 4-bit chunk from the encoded string
        code = encodedStr[i:i+4]
        
        # Look up the 4-bit chunk in the decoding dictionary
        if code in decodeDict:
            decodedStr += decodeDict[code]
        else:
            # Handle the case where an invalid code is encountered
            raise ValueError(f"Invalid Huffman code encountered: {code}")
    
    return decodedStr


# Serial setup
ser = serial.Serial('/dev/cu.usbmodem14301', 115200, timeout=1)
time.sleep(2)

# Queue for thread-safe data exchange
data_queue = queue.Queue()

def serial_reading_thread():

    while True:
        if ser.inWaiting()>0:
            
            byte_data = ser.read(1)
            #print(data)
            process_input(byte_data)
           

def process_input(input_data):
    #convert a byte to a binary string representation
    binary_value = format(ord(input_data), '08b')
    # Print the binary values
    print(f"Received binary data: {input_data}")
    print(f"Received binary data: {binary_value}")

    # Decode the binary string using the Huffman code
    decoded_data = huffman_decode(binary_value, huffmanCode)
    print(f"Received decoded data: {decoded_data}")



    
# Start the serial reading thread
serial_thread = threading.Thread(target=serial_reading_thread, daemon=True)
serial_thread.start()

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

# Function to update the plot
def update(frame):
    while not data_queue.empty():
        line = data_queue.get() 
        #print(line)
        # Parse the line and update the plotting data lists
        data = line.split(',')
        if len(data) >= 13:
            time_data.append(int(data[0]))
            accel_data.append((float(data[1]), float(data[2]), float(data[3])))
            gyro_data.append((float(data[4]), float(data[5]), float(data[6])))
            mag_data.append((float(data[7]), float(data[8]), float(data[9])))
            orientation_data.append((float(data[10]), float(data[11]), float(data[12])))


    # Only plot the latest 100 data points
    # Only plot the latest 100 data points
    range = 100
    # Update plots (similar to previous update function)
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

    #accel
    #this if statement checks if the update object has an attribute called accel_lines, else it creates a new list of lines
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
    ax1.legend(loc='upper left')


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
    ax2.legend(loc='upper left')

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
    ax3.legend(loc='upper left')

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
    ax4.legend(loc='upper left')

    return update.accel_lines + update.gyro_lines + update.mag_lines + update.orientation_lines

# Create animation
ani = animation.FuncAnimation(fig, update, interval=100)

# Show plot
#plt.show()

# Function to log the data at the end
def log_data():
    #wite data to a new csv file
    with open('data/imu_data.csv', 'w') as f:
        f.write('time(ms),accel_x(m/s^2),accel_y(m/s^2),accel_z(m/s^2),gyro_x(rad/s),gyro_y(rad/s),gyro_z(rad/s),mag_x(uT),mag_y(uT),mag_z(uT),orientation_x(degrees),orientation_y(degrees),orientation_z(degrees)\n')
        for i in range(len(time_data)):
            f.write(str(time_data[i]) + ',' + str(accel_data[i][0]) + ',' + str(accel_data[i][1]) + ',' + str(accel_data[i][2]) + ',' + str(gyro_data[i][0]) + ',' + str(gyro_data[i][1]) + ',' + str(gyro_data[i][2]) + ',' + str(mag_data[i][0]) + ',' + str(mag_data[i][1]) + ',' + str(mag_data[i][2]) + ',' + str(orientation_data[i][0]) + ',' + str(orientation_data[i][1]) + ',' + str(orientation_data[i][2]) + '\n')
        
    print('Data logged to imu_data.csv')

# Log the data after the plot window is closed
#log_data()    


