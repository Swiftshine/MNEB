import struct
import numpy as np
import matplotlib.pyplot as plt
import sys

def parse(hex_data):
    if hex_data[0:4].decode() != "MNCH":
        print("Bad file header.")
        sys.exit(1)
    
    plt.figure(figsize=(10, 10))

    num_curves = struct.unpack(">I", hex_data[0xC:0x10])[0]

    current_pos = 0x18
    for i in range(num_curves):
        current_pos = hex_data.find(b"MNCN", current_pos)
        if current_pos == -1: break

        entry_name = hex_data[current_pos + 0x08 : current_pos + 0x28].split(b'\0')[0].decode(errors='ignore')
        
        block_start = current_pos + 0x90
        
        cp_ptr_addr = block_start + 0x0C
        knot_ptr_addr = block_start + 0x10
        
        abs_cp_ptr = struct.unpack(">I", hex_data[cp_ptr_addr : cp_ptr_addr + 4])[0]
        abs_knot_ptr = struct.unpack(">I", hex_data[knot_ptr_addr : knot_ptr_addr + 4])[0]

        num_cp = struct.unpack(">I", hex_data[abs_cp_ptr : abs_cp_ptr + 4])[0]
        cp_data_start = abs_cp_ptr + 4
        
        points_list = []
        for j in range(num_cp):
            ptr = cp_data_start + (j * 8)
            if ptr + 8 <= len(hex_data):
                x, y, z, w = struct.unpack(">hhhh", hex_data[ptr : ptr + 8])
                points_list.append((x, y))

        if points_list:
            pts = np.array(points_list)
            plt.plot(pts[:, 0], pts[:, 1], '-', linewidth=1.5, label=f"{i}: {entry_name}")
            plt.scatter(pts[:, 0], pts[:, 1], s=5)

        current_pos += 4

    plt.axis('equal')
    plt.legend(loc='upper right', fontsize='xx-small')
    plt.grid(True, alpha=0.3)
    plt.title("MNEB Static Renderer (Based on CurveBlock Struct)")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file.mneb>")
    else:
        with open(sys.argv[1], 'rb') as f:
            parse(f.read())