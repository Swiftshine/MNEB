import struct
import re
import numpy as np
import matplotlib.pyplot as plt;
import sys

seek_pos = 0

def seek_relative(amt):
    global seek_pos
    seek_pos += amt

def seek_absolute(amt):
    global seek_pos
    seek_pos = amt

def parse(hex_data):
    if isinstance(hex_data, str):
        hex_data = bytes.fromhex(hex_data.replace(' ', ''))
    
    # check header
    magic = hex_data[0:4].decode()

    if magic != "MNCH":
        print("Bad file header.")
        sys.exit(1)
    
    plt.figure(figsize=(10, 10))
    
    seek_absolute(0xC)

    num_curves = struct.unpack(">I", hex_data[seek_pos:seek_pos + 4])[0]

    seek_absolute(0x18)

    for i in range(num_curves):
        magic = hex_data[seek_pos:seek_pos + 4].decode()

        if magic != "MNCN":
            print(f"Bad entry header @ offset {hex(seek_pos)} (entry ID {i})")
            sys.exit(1)

        seek_relative(4)

        remaining_bytes = struct.unpack(">I", hex_data[seek_pos:seek_pos + 4])[0] - 4 # -4 because we already read the header

        seek_relative(4)
        remaining_bytes -= 4

        name = hex_data[seek_pos:seek_pos + 0x20].split(b'\0')[0].decode()
        print(f"Name: {name}")

        seek_relative(0x20)
        remaining_bytes -= 0x20

        # skip 0x68 bytes for now
        seek_relative(0x68)
        remaining_bytes -= 0x68

        # skip another 0x38 bytes for now
        seek_relative(0x38)
        remaining_bytes -= 0x38

        num_control_points = struct.unpack(">I", hex_data[seek_pos:seek_pos + 4])[0]
        seek_relative(4)
        remaining_bytes -= 4

        control_points = []
        display_points = [] # same as control points, sans z and w
        for j in range(num_control_points):
            control_point = struct.unpack(">hhhh", hex_data[seek_pos:seek_pos + 8])
            control_points.append(control_point)
            seek_relative(8)
            remaining_bytes -= 8
            display_points.append((control_point[0], control_point[1]))
        
        points = np.array(display_points)
        plt.plot(points[:, 0], points[:, 1], '-o', label=name)

        # blah blah blah
        seek_relative(remaining_bytes)
    
    plt.axis('equal')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title("MNEB Parser")
    plt.show()

parse(open(sys.argv[1], 'rb').read())
