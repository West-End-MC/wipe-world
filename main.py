import argparse
import re
from glob import glob
from coordinate import Coordinate
from selection import BlocksSelection, ChunksSelection
import yaml
import sys

def process_coordinates(begin_x, begin_y, begin_z, end_x, end_y, end_z, path, mode):
    mca_files = []
    if path:
        mca_files = glob(f"{path}/*.mca")
        for index in range(len(mca_files)):
            mca_files[index] = re.search(r"r\.-?\d+\.-?\d+\.mca", mca_files[index])[0]

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

def read_residences(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('Residences', {})

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
parser.add_argument("--coords-file", "-c", type=str, help="Path to the file with coordinates")

parser.add_argument("--begin_x", type=int, help="Beginning X coordinate")
parser.add_argument("--begin_y", type=int, help="Beginning Y coordinate")
parser.add_argument("--begin_z", type=int, help="Beginning Z coordinate")
parser.add_argument("--end_x", type=int, help="Ending X coordinate")
parser.add_argument("--end_y", type=int, help="Ending Y coordinate")
parser.add_argument("--end_z", type=int, help="Ending Z coordinate")

args = parser.parse_args()

if not args.coords_file and not (args.begin_x is not None and args.begin_y is not None and args.begin_z is not None and args.end_x is not None and args.end_y is not None and args.end_z is not None):
    parser.error("Either --coords-file must be provided or all coordinate arguments (--begin_x, --begin_y, --begin_z, --end_x, --end_y, --end_z) must be specified.")

if args.coords_file:
    residences = read_residences(args.coords_file)
    for residence_id, residence_info in residences.items():
        area_coords = residence_info['Areas']['main'].split(':')
        begin_x, begin_y, begin_z, end_x, end_y, end_z = map(int, area_coords)
        process_coordinates(begin_x, begin_y, begin_z, end_x, end_y, end_z, args.path, args.mode)
    sys.exit()
else:
    # Проверка, что все координаты были предоставлены
    if None in [args.begin_x, args.begin_y, args.begin_z, args.end_x, args.end_y, args.end_z]:
        parser.error("All coordinate arguments are required if not using --coords-file.")
    process_coordinates(args.begin_x, args.begin_y, args.begin_z, args.end_x, args.end_y, args.end_z, args.path, args.mode)


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