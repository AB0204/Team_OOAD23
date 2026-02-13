
import sys
import zlib
import os
import requests
import string

# PlantUML encoding logic
def encode(data):
    zlibbed = zlib.compress(data.encode('utf-8'))
    compressed = zlibbed[2:-4]
    return encode64(compressed)

def encode64(data):
    _b64 = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
    r = ""
    for i in range(0, len(data), 3):
        if i + 2 == len(data):
            r += append3bytes(data[i], data[i+1], 0)
        elif i + 1 == len(data):
            r += append3bytes(data[i], 0, 0)
        else:
            r += append3bytes(data[i], data[i+1], data[i+2])
    return r

def append3bytes(b1, b2, b3):
    _b64 = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    r = ""
    r += _b64[c1 & 0x3F]
    r += _b64[c2 & 0x3F]
    r += _b64[c3 & 0x3F]
    r += _b64[c4 & 0x3F]
    return r

def generate_diagram(puml_path):
    print(f"Processing {puml_path}...")
    try:
        with open(puml_path, 'r') as f:
            content = f.read()
        
        encoded = encode(content)
        url = f"http://www.plantuml.com/plantuml/png/{encoded}"
        
        response = requests.get(url)
        if response.status_code == 200:
            output_path = puml_path.replace('.puml', '.png')
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Success: Saved to {output_path}")
        else:
            print(f"Error: Server returned {response.status_code} for {puml_path}")
            
    except Exception as e:
        print(f"Exception for {puml_path}: {e}")

files = [
    "/Users/abhiabhardwaj/Analysis/Select_Season_Race_Session.puml",
    "/Users/abhiabhardwaj/Analysis/Select_Drivers.puml",
    "/Users/abhiabhardwaj/Analysis/View_Lap_Time_Comparison.puml",
    "/Users/abhiabhardwaj/Analysis/View_Position_Over_Laps.puml",
    "/Users/abhiabhardwaj/Analysis/View_Tyre_Stints.puml"
]

for f in files:
    generate_diagram(f)
