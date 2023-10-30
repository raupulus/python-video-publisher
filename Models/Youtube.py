#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from oauth2client import client, GOOGLE_TOKEN_URI

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

class Youtube:
    # Maximum number of times to retry before giving up.
    MAX_RETRIES = 10

    # Always retry when these exceptions are raised.
    RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

    # Always retry when an apiclient.errors.HttpError code raised
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    CLIENT_SECRETS_FILE = "client_secrets.json"
    YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    # This variable defines a message to display if the CLIENT_SECRETS_FILE is missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:

    %s

    with information from the API Console
    https://console.cloud.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__),CLIENT_SECRETS_FILE))

    VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

    def upload(self, options):

        if options.get('tags') and isinstance(options.get('tags'), str):
            options['tags'] = options.get('tags').split(",")

        if options.get('privacy_status') and not options.get('privacy_status') in self.VALID_PRIVACY_STATUSES:
            options['privacy_status'] = self.VALID_PRIVACY_STATUSES[1]

        if not os.path.exists(options.get('file')):
            print("Please specify a valid file path.")

            return None

        youtube = self.get_authenticated_service(options)

        try:
            return self.initialize_upload(youtube, options)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

            ## Almaceno error en el histórico
            write_file = open("error.log", "a")
            write_file.write("\n\nAn HTTP error %d occurred:\n%s\n\n" % (e.resp.status, e.content))
            write_file.close()

            return None

    def get_authenticated_service(self, args):
        flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
                                    scope=self.YOUTUBE_UPLOAD_SCOPE,
                                    message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()


        """
        class obj(object):
            def __init__(self, d):
                for k, v in d.items():
                    if isinstance(k, (list, tuple)):
                        setattr(self, k, [obj(x) if isinstance(x, dict) else x for x in v])
                    else:
                        setattr(self, k, obj(v) if isinstance(v, dict) else v)
        """

        #args = obj(args)
        #args = argparser.parse_args()

        print(args)


        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, args)

            """
            credentials = client.OAuth2Credentials(
                access_token = credentials.access_token,
                client_id = credentials.client_id,
                client_secret = credentials.client_secret,
                refresh_token = credentials.refresh_token,
                token_expiry = credentials.token_expiry,
                token_uri = GOOGLE_TOKEN_URI,
                user_agent= "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/118.0",
                revoke_uri= None)
            """

        return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))


    def initialize_upload(self, youtube, options):
        body = dict(
            snippet=dict(
                title=options.get('title'),
                description=options.get('description'),
                tags=options.get('tags'),
                categoryId=options.get('category'),

            ),
            status=dict(
                privacyStatus=options.get('privacy_status')
            )
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(options.get('file'), chunksize=-1, resumable=True)
        )

        return self.resumable_upload(insert_request)

    # This method implements an exponential backoff strategy to resume a
    # failed upload.

    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0

        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        #print(f"Response: {response}")
                        #print("Video id '%s' was successfully uploaded." % response['id'])
                        return response['id']
                    else:
                        print("The upload failed with an unexpected response: %s" % response)

                        return None
            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
                else:
                    raise
            except self.RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1

                if retry > self.MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep

                print("Sleeping %f seconds and then retrying..." % sleep_seconds)

                time.sleep(sleep_seconds)
