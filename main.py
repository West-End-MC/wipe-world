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

parser.add_argument("begin-x", type=int)
parser.add_argument("begin-y", type=int)
parser.add_argument("begin-z", type=int)
parser.add_argument("end-x",   type=int)
parser.add_argument("end-y",   type=int)
parser.add_argument("end-z",   type=int)

args = parser.parse_args()

if args.selection == "out" and args.path is None:
    parser.error("--path is required if --mode is \"out\".")

beg = { x: args.begin_x, y:args.begin_y, args.begin_z }
end = { x: args.end_x, y:args.end_y, args.end_z }
