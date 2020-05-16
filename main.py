import argparse
import re
from glob import glob

parser = argparse.ArgumentParser(description='Browse mca files using block/chunk coordenates.')
parser.add_argument("--selection", "-s", choices=["in", "out"], default="in", 
                    help="""
                         Defines selection mode (default: "%(default)s")
                         in =>  Will find all the mca files that are within the coordinate range.
                         out => will find all the mca files that are outside the coordinate range.
                         """)
parser.add_argument("--path", "-p", type=str, 
                    help="""
                         Required if "--mode" is "out".
                         If defined, it will show only the mca files that are inside the folder.
                         If not defined, it will show all possible mca files.
                         """)
parser.add_argument("--mode", "-m", type=str, choices=["blocks", "chunks"], default="blocks")

parser.add_argument("begin_x", type=int)
parser.add_argument("begin_y", type=int)
parser.add_argument("begin_z", type=int)
parser.add_argument("end_x",   type=int)
parser.add_argument("end_y",   type=int)
parser.add_argument("end_z",   type=int)

args = parser.parse_args()

if args.selection == "out" and args.path is None:
    parser.error("--path is required if --mode is \"out\".")

mca_files = []
if args.path:
    mca_files = glob("%s/*.mca"%(args.path))
    for index in range(len(mca_files)):   
        mca_files[index] = re.search("r\\.-?\\d+\\.-?\\d+\\.mca", mca_files[index])[0]

coordenates = [ { "x": args.begin_x, "y": args.begin_y, "z": args.begin_z },
                { "x": args.end_x,   "y": args.end_y,   "z": args.end_z } ]

min_block   = { "x": 0, "y": 0, "z": 0 }
max_block   = { "x": 0, "y": 0, "z": 0 }

min_chunk   = { "x": 0, "y": 0, "z": 0 }
max_chunk   = { "x": 0, "y": 0, "z": 0 }

# Ensuring that the axes are ordered from smallest to largest.
for axis in ("x", "y", "z"):
    if coordenates[0][axis] > coordenates[1][axis]:
        temp = coordenates[0][axis]
        coordenates[0][axis] = coordenates[1][axis]
        coordenates[1][axis] = temp

# Convert blocks to chunks.
if args.mode == "blocks":
    for index in range(len(coordenates)):
        for axis in ("x", "y", "z"):
            coordenates[index][axis] = coordenates[index][axis] >> 4

for axis in ("x", "y", "z"):
    min_block[axis] =  coordenates[0][axis] << 4
    max_block[axis] = (coordenates[1][axis] + 1 << 4) - 1

# Convert chunks to regions.
for index in range(len(coordenates)):
    for axis in ("x", "y", "z"):
        coordenates[index][axis] = coordenates[index][axis] >> 5

for axis in ("x", "y", "z"):
    min_chunk[axis] =  coordenates[0][axis] << 5
    max_chunk[axis] = (coordenates[1][axis] + 1 << 5) - 1

mca_list = []
for x in range(coordenates[0]["x"],coordenates[1]["x"] + 1):
    for z in range(coordenates[0]["z"],coordenates[1]["z"] + 1):
        mca_list += ["r.%s.%s.mca"%(x,z)]

print(
"""
----------------------
Number of possible .mca files: %s
List of files based in a real folder?: %s
==
Block coordenates: "%s %s %s" to "%s %s %s"
Chunk coordenates: "%s 0 %s" to "%s 0 %s"
==
----------------------
"""%(len(mca_list), "Yes" if args.path else "No",
   min_block["x"], min_block["y"], min_block["z"],
   max_block["x"], max_block["y"], max_block["z"],
   min_chunk["x"], min_chunk["z"],
   max_chunk["x"], max_chunk["z"]))

if args.path:
    print("Showing .mca files from \"%s\" that are ->%s<- the indicated coordinates:\n"
          %(args.path, "WITHIN" if args.selection == "in" else "OUTSIDE"))
    if args.selection == "in":
        temp_mca_list = mca_list
        mca_list = []
        for mca_file in mca_files:
            if mca_file in temp_mca_list: mca_list += [mca_file]
    else:
        for mca_file in mca_files:
            if mca_file in mca_list: mca_list.remove(mca_file)
else:
    print("Showing all the possible .mca files that can be generated ->WITHIN< the indicated coordinates:\n")

mca_text = ""
for mca in mca_list:
    mca_text += "'%s' "%(mca)
print("%s\n"%(mca_text))