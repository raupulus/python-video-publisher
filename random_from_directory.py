#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import argparse
from time import sleep
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv("DEBUG")

# Parse command line arguments
parser = argparse.ArgumentParser(description='Process some files.')
parser.add_argument('--file', type=str, default=os.getenv("INPUT_PATH"),
                    help='an input file directory')
parser.add_argument('--move-to', type=str, default=os.getenv("OUTPUT_PATH"),
                    help='a destination directory')
parser.add_argument('--quantity', type=int,
                    default=int(os.getenv("RANDOM_QUANTITY")),
                    help='the quantity of videos')
parser.add_argument('--random-off', action='store_true',
                    help='disable random selection of files')

args = parser.parse_args()


video_extensions = (".mp4", ".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".m4v")

# Use arguments
INPUT_PATH = args.file
OUTPUT_PATH = args.move_to
RANDOM_QUANTITY = args.quantity

files = [os.path.join(INPUT_PATH, f) for f in os.listdir(INPUT_PATH) if
         os.path.isfile(os.path.join(INPUT_PATH, f)) and f.endswith(
             video_extensions)]

if not files or not len(files):
    print("No se encontraron archivos válidos")
    exit(0)

# Add conditional random selection
if args.random_off:
    files.sort()  # sort files in ascending order by name
    selected_files = files[:RANDOM_QUANTITY]
else:
    selected_files = random.sample(files,
                                   RANDOM_QUANTITY if RANDOM_QUANTITY < len(
                                       files) else len(files))

print("Selected files:")
print(selected_files)

print("Ejecutando comando principal...")
print(f"Archivos seleccionados: {selected_files}")
print(f"Salida: '{OUTPUT_PATH}'")

for file in selected_files:
    print('Ejecutando comando: python3 main.py --file="%s" --move-to=\'%s\'' % (
    file, OUTPUT_PATH))
    os.system(f"python3 main.py --file=\"{file}\" --move-to=\'{OUTPUT_PATH}\'")

    # Add conditional sleep
    if RANDOM_QUANTITY > 1:
        sleep(random.randint(37, 158))
    else:
        sleep(5)  # Wait for 5 seconds if RANDOM_QUANTITY equals 1
