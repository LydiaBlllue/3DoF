import os
import glob
import pandas as pd

#combine all csv files in folder into one csv file
path1 = "/Users/lin/Desktop/Work/3DoF/imu_data/2.2/Accelerometer.csv"
path2 = "/Users/lin/Desktop/Work/3DoF/imu_data/2.2/Gyroscope.csv"
path3 = "/Users/lin/Desktop/Work/3DoF/imu_data/2.2/Magnetometer.csv"

combinedcsv = "/Users/lin/Desktop/Work/3DoF/imu_data/2.2/combined.csv"

#combine Accelerometer.csv Gyroscope.csv Magnetometer.csv into one csv file
# use time as index drop seconds_elapsed column
# rename columns to include sensor name

df1 = pd.read_csv(path1, index_col='time', parse_dates=True)

df2 = pd.read_csv(path2, index_col='time', parse_dates=True)

df3 = pd.read_csv(path3, index_col='time', parse_dates=True)

df1 = df1.drop(columns=['seconds_elapsed'])
df2 = df2.drop(columns=['seconds_elapsed'])
df3 = df3.drop(columns=['seconds_elapsed'])

df1 = df1.rename(columns={'x': 'Acc_x', 'y': 'Acc_y', 'z': 'Acc_z'})
df2 = df2.rename(columns={'x': 'Gyro_x', 'y': 'Gyro_y', 'z': 'Gyro_z'})
df3 = df3.rename(columns={'x': 'Mag_x', 'y': 'Mag_y', 'z': 'Mag_z'})

df = pd.concat([df1, df2, df3], axis=1, join='inner')

df.to_csv(combinedcsv, index=True, header=True)




