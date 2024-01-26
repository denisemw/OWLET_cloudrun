#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:59:03 2023

@author: werchd01
"""

# Copyright 2019 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_imageproc_controller]
import base64
import json
import os
import tempfile


from flask import Flask
from google.cloud import storage
import sys
sys.path.append("eyetracker")

import argparse
from run_owlet import OWLET
from pathlib import Path


app = Flask(__name__)



#@app.route("/", methods=["POST"])
def index():
    print("started")
    """  storage_client = storage.Client("owlet-app")
    bucket = storage_client.get_bucket("owlet-app.appspot.com")
    blob = bucket.blob("videos/sbBb1AjbYzmQ1f4eAUuL.mp4")

    _, temp_local_filename = tempfile.mkstemp() """

    
    # Download the file to a destination
        # blob.download_to_filename(temp_local_filename)
        # print(temp_local_filename)
    storage_client = storage.Client("owlet-app")
    bucket = storage_client.get_bucket("owlet-app.appspot.com")
    blob = bucket.blob("upload_test/test.csv")
    blob.download_to_filename("Users\werchd01\cloudruntestcsv.csv")

    #owlet = OWLET()
    #owlet.process_subject() 
        
         

    #     return ("", 204)

    # except Exception as e:
    #     print(f"error: {e}")
    #     return ("", 500)
    





    #Receive and parse Pub/Sub messages containing Cloud Storage event data."""
""" 
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    # Decode the Pub/Sub message.
    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        try:
            data = json.loads(base64.b64decode(pubsub_message["data"]).decode())

        except Exception as e:
            msg = (
                "Invalid Pub/Sub message: "
                "data property is not valid base64 encoded JSON"
            )
            print(f"error: {e}")
            return f"Bad Request: {msg}", 400

        # Validate the message is a Cloud Storage event.
        if not data["name"] or not data["bucket"]:
            msg = (
                "Invalid Cloud Storage notification: "
                "expected name and bucket properties"
            )
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        try:
            
            file_name = data["name"]
            bucket_name = data["<mybucketname>"]
            owlet = OWLET()
            # get the blob from the storage bucket
            blob = storage_client.bucket(bucket_name).get_blob(file_name)
            # make a temporary local file
            _, temp_local_filename = tempfile.mkstemp()

            # Download file from bucket.
            blob.download_to_filename(temp_local_filename)
            
            # process the file
            owlet.calibrate_gaze(temp_local_filename)
            owlet.process_subject(temp_local_filename)            
                
            return ("", 204)

        except Exception as e:
            print(f"error: {e}")
            return ("", 500)

    return ("", 500)
 """
    # [END cloudrun_imageproc_controller]


if __name__ == "__main__":
    index()
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
   # app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
