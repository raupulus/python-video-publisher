#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from tiktok_uploader.upload import upload_video, upload_videos
from tiktok_uploader.auth import AuthBackend

load_dotenv()

class TikTok:
    def __init__(self):
        self.DEBUG = os.getenv("DEBUG")
        self.COOKIES = 'tiktok_cookies.txt'

    def upload(self, options):
        print("Uploading video to TikTok...")

        upload_video(filename=options.get('file'),
            description=options.get('title'),
            cookies=self.COOKIES,
            headless=True)
