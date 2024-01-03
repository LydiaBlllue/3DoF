import serial
import sys

# Replace with your Huffman tree or mapping
HUFFMAN_TABLE = {
    
    # chars: 0,1,2,3,4,5,6,7,8,9,.,',','<','>','-'
    #length of the code: 4
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
    '-': '1111'


}

def decode_huffman(encoded_str, huffman_table):
    """Decode a Huffman encoded string using the provided Huffman table."""
    decoded_str = ''
    code = ''
    for bit in encoded_str:
        code += bit
        if code in huffman_table:
            decoded_str += huffman_table[code]
            code = ''
    return decoded_str

def read_from_serial(ser):
    """Read data from serial and return the decoded and parsed data."""
    buffer = ''
    while True:
        if ser.in_waiting > 0:
            byte = ser.read().decode('utf-8')
            print("Byte:", byte)
        

def main():
    # Set up serial connection (adjust the port and baudrate as needed)
    ser = serial.Serial('/dev/cu.usbmodem14201', 115200, timeout=1)
    try:
        while True:
            data_points = read_from_serial(ser)
            print("Decoded Data:", data_points)
    except KeyboardInterrupt:
        print("Interrupted by the user")
        ser.close()
        sys.exit()

if __name__ == "__main__":
    main()
