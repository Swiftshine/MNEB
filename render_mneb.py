# note - this code uses heuristics instead of referencing the actual structure.
# it correctly displays an MNEB file, but not necessarily in the right way.

import struct
import re
import numpy as np
import matplotlib.pyplot as plt
import sys

def parse_mneb_universal(hex_data):
    if isinstance(hex_data, str):
        hex_data = bytes.fromhex(hex_data.replace(' ', ''))
    
    plt.figure(figsize=(10, 10))
    matches = list(re.finditer(b'MNCN', hex_data))
    
    for match in matches:
        base = match.start()
        name = hex_data[base+8:base+24].split(b'\0')[0].decode(errors='ignore')

        data_pos = -1
        cv_count = 0
        
        for p in range(base + 0x80, base + 0x300, 2):
            if p + 6 < len(hex_data):
                if hex_data[p+4:p+6] == b'\xFF\x64':
                    cv_count = struct.unpack(">I", hex_data[p-4:p])[0]
                    if 0 < cv_count < 500: # sanity check
                        data_pos = p
                        break
        
        if data_pos != -1:
            points = []
            for i in range(cv_count):
                offset = data_pos + (i * 8)
                if offset + 8 > len(hex_data): break
                x, y, z, w = struct.unpack(">hhhh", hex_data[offset:offset+8])
                points.append((x, y))
            
            pts = np.array(points)
            plt.plot(pts[:, 0], pts[:, 1], '-o', markersize=2, label=name)
            print(f"Parsed {name}: {cv_count} points at {hex(data_pos)}")

    plt.axis('equal')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title("Universal MNEB Parser")
    plt.show()

parse_mneb_universal(open(sys.argv[1], "rb").read())
