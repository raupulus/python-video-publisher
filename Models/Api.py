#! /usr/bin/env python3

import requests
from dotenv import load_dotenv
import os
import json
from time import sleep

load_dotenv()

class Api:
    headers = {
        'Authorization': 'Bearer ' + os.getenv("API_KEY"),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def __init__(self):
        self.debug = os.getenv("DEBUG")
        self.api_key = os.getenv("API_KEY")
        self.url = os.getenv("API_URL")

    def update_video_info(self, params):
        errors = 0
        max_retries = 5

        while errors < max_retries:
            try:
                response = requests.post(url=self.url, json=params, headers=self.headers)
                break
            except Exception as e:
                print("Error al actualizar información del vídeo")
                print(e)
                errors += 1
                sleep(5)

        if response.status_code != 200:
            print("Error al actualizar información del vídeo")
            print("API http_status: ", response.status_code)
            print("API Contenido: ", response.text)

            return None

        return response.json()
