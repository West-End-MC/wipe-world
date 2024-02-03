import argparse
import re
from glob import glob
from datetime import datetime, timedelta
from os.path import getmtime, basename
import os
import yaml
from coordinate import Coordinate
from selection import BlocksSelection, ChunksSelection

# Вспомогательная функция для чтения данных резиденций
def read_residences(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('Residences', {})

# Вспомогательная функция для определения, старше ли файл 5 месяцев
def is_file_older_than(file_path, months=5):
    file_mod_time = datetime.fromtimestamp(getmtime(file_path))
    cutoff_date = datetime.now() - timedelta(days=30 * months)
    return file_mod_time < cutoff_date

# Основная функция обработки координат и вывода информации
def process_coordinates(begin_x, begin_y, begin_z, end_x, end_y, end_z, path, mode, residence_name, founder_name):
    mca_files = []
    if path:
        mca_files = glob(f"{path}/*.mca")
        mca_files = [re.search("r\\.-?\\d+\\.-?\\d+\\.mca", mca_file)[0] for mca_file in mca_files if re.search("r\\.-?\\d+\\.-?\\d+\\.mca", mca_file)]
    
    selection = BlocksSelection(Coordinate(begin_x, begin_y, begin_z), Coordinate(end_x, end_y, end_z)) if mode == "blocks" else ChunksSelection(Coordinate(begin_x, begin_y, begin_z), Coordinate(end_x, end_y, end_z))
    selection = selection.toRegionsSelection()

    mca_list = [f"r.{region.x}.{region.z}.mca" for region in selection]
    print_output(mca_list, path, selection, args.selection, residence_name, founder_name)
    return set(mca_list)  # Возвращаем множество для упрощения сравнения

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

# Настройка аргументов скрипта
parser = argparse.ArgumentParser(description='Process .mca files based on residence coordinates.')
parser.add_argument("--selection", "-s", choices=["in", "out"], default="in")
parser.add_argument("--path", "-p", type=str, help="Path to the .mca files directory.")
parser.add_argument("--mode", "-m", choices=["blocks", "chunks"], default="blocks")
parser.add_argument("--coords-file", "-c", type=str, help="Path to the YAML file with residences.")

args = parser.parse_args()

if args.coords_file and args.path:
    files_to_keep = set()
    residences = read_residences(args.coords_file)
    for residence_name, residence_info in residences.items():
        area_coords = residence_info['Areas']['main'].split(':')
        founder_name = residence_info.get('OwnerLastKnownName', 'Unknown')
        files_for_residence = process_coordinates(*map(int, area_coords), args.path, args.mode, residence_name, founder_name)
        files_to_keep.update(files_for_residence)

    all_mca_files = {basename(file_path): file_path for file_path in glob(f"{args.path}/*.mca")}
    for file_name, file_path in all_mca_files.items():
        if file_name not in files_to_keep and is_file_older_than(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")

else:
    print("Error: Both --coords-file and --path arguments are required.")
    sys.exit(1)