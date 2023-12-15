#include <iostream>
#include <vector>

#include "rapidcsv.h"
#include "MadgwickAHRS.h" 

Madgwick filter;


int main() {
    // Read a line of data from the CSV
    rapidcsv::Document doc("imu_data/2.2/combined.csv");
    //sey a counter to 0
    int counter = 0;

    std::ofstream outFile("orientation_data.csv");
    outFile << "Roll,Pitch,Yaw\n";


    while (counter<doc.GetRowCount()){
        //get the data from the csv
        std::vector<float> row = doc.GetRow<float>(counter);
        //update the filter with the data
        filter.update(row[4], row[5], row[6], row[1], row[2], row[3], row[7], row[8], row[9]);
        //get the orientation from the filter
        float roll = filter.getRoll();
        float pitch = filter.getPitch();
        float Yaw = filter.getYaw();

        //print the orientation
        std::cout << "roll: " << roll << " pitch: " << pitch << " Yaw: " << Yaw << std::endl;

        outFile << roll << "," << pitch << "," << Yaw << "\n";

        //increment the counter
        counter++;
    }
    outFile.close();
    
    return 0;
}
