#!/usr/bin/env python

import os
import json
import argparse
from dotenv import load_dotenv
from Models.Youtube import Youtube
from Models.Api import Api

load_dotenv()

DEBUG = os.getenv("DEBUG")
API_UPLOAD = os.getenv("API_UPLOAD")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")

parser = argparse.ArgumentParser(description="Tool for upload video to Youtube", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--file", help="Archivo de vídeo a subir", required=True)
parser.add_argument("--move-to", help="Directorio donde se moverá el archivo de vídeo subido", default=None)

args = parser.parse_args()
config = vars(args)

file = config.get('file')
file_name = file.split('/')[-1]
move_to = config.get('move_to') or OUTPUT_PATH
title = file.split('.')[0].split('/')[-1]
file_json = file.replace(file.split('.')[-1], 'json')
file_md = file.replace(file.split('.')[-1], 'md')
file_txt = file.replace(file.split('.')[-1], 'txt')
json_data = None

if not os.path.isfile(file):
    print('File Video not found')
    exit(1)

if not os.path.isfile(file_json):
    file_json = None
    print('File JSON not found')

if not os.path.isfile(file_md):
    file_md = None
    print('File MD not found')

if not os.path.isfile(file_txt):
    file_txt = None
    print('File MD not found')

description = ""

if file_json:
    with open(file_json, 'r') as f:
        json_data = json.load(f)

if json_data:
    description += json_data.get('description')
    description += "\n\nEach image in this video has been generated with Stable Diffusion in an automated way, trying to be unique in the world.\nThe description to create the image is generated from models trained by Roles with a pattern of randomness using different AIs such as GPT Instruct.\nOnce I have generated a batch of images with different seeds for the same description, I use ffmpeg to also automatically generate this video.\n\nWesite with all images and seeds: https://aidyslexic.raupulus.dev\nTwitter: https://twitter.com/ai_automations\nAuthor Website: https://raupulus.dev\nTool for generate prompts: https://github.com/raupulus/python-ai-image-from-api-generator\nTool ffmpeg slideshow: https://github.com/raupulus/ffmpeg-slideshow-from-image-directory\n\n"

if file_txt:
    with open(file_txt, 'r') as f:
        description += f.read()
elif file_md:
    with open(file_md, 'r') as f:
        description += f.read()

tags = json_data.get('tags') if json_data else []

if not tags and json_data.get('metatags'):
    tags = json_data.get('metatags')

options = {
    "file": file,
    "title": json_data.get('title') if json_data else title,
    "description": description,
    "video_file": file,
    "privacy_status": "public",
    "category": "22",
    "tags": json_data.get('tags') if json_data else []
}

youtube = Youtube()
video_id = youtube.upload(options)

if video_id:
    print("Video uploaded successfully! ID: " + video_id)

if video_id and API_UPLOAD and json_data.get('batch_id'):
    params = {
        "batch_id": json_data.get('batch_id'),
        "video_id": video_id,
        "url_youtube": "https://www.youtube.com/embed/" + video_id,
    }

    api = Api()
    api.update_video_info(params)


if video_id and move_to:
    os.rename(file, move_to + '/' + file_name)

    if file_json:
        os.rename(file_json, move_to + '/' + file_name.replace(file_name.split('.')[-1], 'json'))

    if file_md:
        os.rename(file_md, move_to + '/' + file_name.replace(file_name.split('.')[-1], 'md'))

    if file_txt:
        os.rename(file_txt, move_to + '/' + file_name.replace(file_name.split('.')[-1], 'txt'))

    print("File moved successfully!")


exit(0)
