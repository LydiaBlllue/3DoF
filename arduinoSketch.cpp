#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define BNO055_SAMPLERATE_DELAY_MS 10
#define SENSOR_ADDRESS 0x28

// Huffman codes for each character
struct HuffmanCode {
    char character;
    uint8_t code;  // Now a byte representing the binary code
};


Adafruit_BNO055 bno = Adafruit_BNO055(55, SENSOR_ADDRESS, &Wire);

unsigned long lastReadTime = 0;


// Define the number of mappings you have
#define NUM_CODES 15

#define NUM_CODES 15

HuffmanCode huffmanMap[NUM_CODES] = {
    {'0', 0b0000},
    {'1', 0b0001},
    {'2', 0b0010},
    {'3', 0b0011},
    {'4', 0b0100},
    {'5', 0b0101},
    {'6', 0b0110},
    {'7', 0b0111},
    {'8', 0b1000},
    {'9', 0b1001},
    {',', 0b1010},
    {'.', 0b1011},
    {'<', 0b1100},
    {'>', 0b1110},
    {'-', 0b1111}
};


const char* getHuffmanCode(char character) {
    for (int i = 0; i < NUM_CODES; ++i) {
        if (huffmanMap[i].character == character) {
            return huffmanMap[i].code;
        }
    }
    return NULL; // Return NULL or some indication that the character wasn't found
}


// Encode if input is a single character
uint8_t encodeValue(char value){
  for (int i = 0; i < NUM_CODES; ++i) {
        if (huffmanMap[i].character == value) {
            return huffmanMap[i].code;
        }
    }
    return 0; 
}
// Encode if input is string use encodeValue(char value)
uint8_t encodeValue(char* value){
  uint8_t result = 0;
  for (int i = 0; i < strlen(value); ++i) {
        result = result << 4;
        result = result | encodeValue(value[i]);
    }
    return result;
  
}

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  
}


void loop(){
  Serial.write(encodeValue('1'));
  Serial.write(encodeValue('2'));
  Serial.write(encodeValue('3'));
  Serial.write(encodeValue('4'));
  Serial.write(encodeValue('5'));
}