#!/usr/bin/env python

import os
from dotenv import load_dotenv
import random

load_dotenv()

DEBUG = os.getenv("DEBUG")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
RANDOM_QUANTITY = int(os.getenv("RANDOM_QUANTITY"))
INPUT_PATH = os.getenv("INPUT_PATH")

video_extensions = (".mp4", ".mov", ".avi", ".wmv", ".flv", ".mkv", ".webm", ".m4v")

## Busco en el directorio de entrada archivos con extensión válida
files = [os.path.join(INPUT_PATH, f) for f in os.listdir(INPUT_PATH) if os.path.isfile(os.path.join(INPUT_PATH, f)) and f.endswith(video_extensions)]

if not files or not len(files):
    print("No se encontraron archivos válidos")
    exit(0)

## Obtengo varios archivos aleatorios
random_files = random.sample(files, RANDOM_QUANTITY)

print(random_files)
