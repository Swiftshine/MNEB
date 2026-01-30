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
    
    global_min_x, global_max_x = float('inf'), float('-inf')
    global_min_y, global_max_y = float('inf'), float('-inf')

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

        if points.size > 0:
            # calculate local extremes for the current curve
            local_min = points.min(axis=0)
            local_max = points.max(axis=0)
            
            # update global extremes
            global_min_x = min(global_min_x, local_min[0])
            global_max_x = max(global_max_x, local_max[0])
            global_min_y = min(global_min_y, local_min[1])
            global_max_y = max(global_max_y, local_max[1])

        plt.plot(points[:, 0], points[:, 1], '-o', label=name)

        # blah blah blah
        seek_relative(remaining_bytes)
    
    print("-" * 30)
    print(f"Global Extremes:")
    print(f"X range: [{global_min_x}, {global_max_x}] (Delta: {global_max_x - global_min_x})")
    print(f"Y range: [{global_min_y}, {global_max_y}] (Delta: {global_max_y - global_min_y})")
    print("-" * 30)

    plt.axis('equal')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title("MNEB Render")
    plt.show()

parse(open(sys.argv[1], 'rb').read())
