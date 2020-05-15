import argparse
import re
parser = argparse.ArgumentParser(description='Browse mca files using block/chunk coordenates.')
parser.add_argument("--mode", "-m", choices=["in", "out"], default="in", 
                    help="""
                         Defines selection mode (default: "%(default)s")
                         in =>  Will find all the mca files that are within the coordinate range.
                         out => will find all the mca files that are outside the coordinate range.
                         """)
parser.add_argument("--path", "-p", type=str, 
                    help="""
                         If defined, it will show only the mca files that are inside the folder.
                         If not defined, it will show all possible mca files.
                         """)

subparsers = parser.add_subparsers()
parser_block = subparsers.add_parser('block')
parser_chunk = subparsers.add_parser('chunk')

parser_block.add_argument("begin-x", type=int)
parser_block.add_argument("begin-y", type=int)
parser_block.add_argument("begin-z", type=int)
parser_block.add_argument("end-x", type=int)
parser_block.add_argument("end-y", type=int)
parser_block.add_argument("end-z", type=int)

parser_chunk.add_argument("begin-x", type=int)
parser_chunk.add_argument("begin-z", type=int)
parser_chunk.add_argument("end-x", type=int)
parser_chunk.add_argument("end-z", type=int)

args = parser.parse_args()