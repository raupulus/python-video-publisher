#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from time import sleep
from dotenv import load_dotenv

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
random_files = random.sample(files, RANDOM_QUANTITY if RANDOM_QUANTITY < len(files) else len(files))

print(random_files)


print("Ejecutando comando principal...")
print(f"Archivos aleatorios: {random_files}")
print(f"Salida: \'{OUTPUT_PATH}\'")

## Ejecuto el comando principal enviando los archivos aleatorios
for file in random_files:
    print('Ejecutando comando: python3 main.py --file=\'%s\' --move-to=\'%s\'' % (file, OUTPUT_PATH))
    os.system(f"python3 main.py --file=\'{file}\' --move-to=\'{OUTPUT_PATH}\'")

    ## Espero un tiempo aleatorio antes de ejecutar el siguiente comando
    sleep(random.randint(37, 158))
