import argparse

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
