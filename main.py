import argparse
import re
from glob import glob
from coordinate import Coordinate
from selection import BlocksSelection, ChunksSelection
import yaml
import sys

# Функция чтения резиденций
def read_residences(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('Residences', {})

# Определение аргументов скрипта
parser = argparse.ArgumentParser(description='Browse mca files using block/chunk coordinates.')
parser.add_argument("--selection", "-s", choices=["in", "out"], default="in")
parser.add_argument("--path", "-p", type=str)
parser.add_argument("--mode", "-m", choices=["blocks", "chunks"], default="blocks")
parser.add_argument("--coords-file", "-c", type=str, help="Path to the file with coordinates")

args = parser.parse_args()

# Функция обработки координат
def process_coordinates(begin_x, begin_y, begin_z, end_x, end_y, end_z, path, mode, residence_name, founder_name):
    mca_files = []
    print_output(mca_list, path, selection, args.selection, residence_name, founder_name)
    if path:
        mca_files = glob(f"{path}/*.mca")
        mca_files = [re.search("r\\.-?\\d+\\.-?\\d+\\.mca", mca_file)[0] for mca_file in mca_files if re.search("r\\.-?\\d+\\.-?\\d+\\.mca", mca_file)]
    
    selection = BlocksSelection(Coordinate(begin_x, begin_y, begin_z), Coordinate(end_x, end_y, end_z)) if mode == "blocks" else ChunksSelection(Coordinate(begin_x, begin_y, begin_z), Coordinate(end_x, end_y, end_z))
    selection = selection.toRegionsSelection()

    mca_list = [f"r.{region.x}.{region.z}.mca" for region in selection]
    print_output(mca_list, path, selection, args.selection)

# Функция для вывода результатов
def print_output(mca_list, path, selection, selection_mode, residence_name, founder_name):
    print(f"""
------------------------------------
Residence: {residence_name}
Founder: {founder_name}
Number of possible .mca files: {len(mca_list)}
List of files based in a real folder?: {"Yes" if path else "No"}

== SELECTION DETAILS ==
Block coordinates: "{selection.toBlocksSelection()}"
Chunk coordinates: "{selection.toChunksSelection()}"
=======================
------------------------------------
""")

    if path:
        print(f"Showing .mca files from \"{path}\" that are ->{'WITHIN' if selection_mode == 'in' else 'OUTSIDE'}<- the indicated coordinates:\n")
        mca_text = " ".join(f"'{mca}'" for mca in mca_list)
        print(f"{mca_text}\n")

# Обработка координат из файла
if args.coords_file:
    residences = read_residences(args.coords_file)
    for residence_name, residence_info in residences.items():
        area_coords = residence_info['Areas']['main'].split(':')
        founder_name = residence_info.get('OwnerLastKnownName', 'Unknown')
        process_coordinates(*map(int, area_coords), args.path, args.mode, residence_name, founder_name)
    sys.exit()

# Если скрипт не завершился после обработки файла, значит была ошибка в логике или вводе
print("Error: Check your input or logic.")
