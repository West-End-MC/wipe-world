import argparse
import re
from glob import glob
from coordinate import Coordinate
from classes import BlocksSelection, ChunksSelection

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

selection = None
if args.mode == "blocks":
    selection = BlocksSelection(Coordinate(args.begin_x,args.begin_y,args.begin_z), Coordinate(args.end_x,args.end_y,args.end_z))
else:
    selection = ChunksSelection(Coordinate(args.begin_x,args.begin_y,args.begin_z), Coordinate(args.end_x,args.end_y,args.end_z))
selection = selection.toRegionsSelection()

mca_list = ["r.%s.%s.mca"%(region.x, region.z) for region in selection]
print(
"""
------------------------------------
Number of possible .mca files: %s
List of files based in a real folder?: %s

== SELECTION DETAILS ==
Block coordenates: "%s"
Chunk coordenates: "%s"
=======================
------------------------------------
"""%(len(mca_list), "Yes" if args.path else "No", selection.toBlocksSelection(), selection.toChunksSelection()))

if args.path:
    print("Showing .mca files from \"%s\" that are ->%s<- the indicated coordinates:\n"
          %(args.path, "WITHIN" if args.selection == "in" else "OUTSIDE"))
    if args.selection == "in":
        temp_mca_list = mca_list
        mca_list = []
        for mca_file in mca_files:
            if mca_file in temp_mca_list: mca_list += [mca_file]
    else:
        for mca in mca_list:
            if mca in mca_files: mca_files.remove(mca)
        mca_list = mca_files
else:
    print("Showing all the possible .mca files that can be generated ->WITHIN< the indicated coordinates:\n")

mca_text = ""
for mca in mca_list:
    mca_text += "'%s' "%(mca)
print("%s\n"%(mca_text))