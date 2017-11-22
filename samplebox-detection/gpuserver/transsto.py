#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from google.cloud import storage

BUCKET_NAME = 'sweetsdetection'
STORAGE_PATH = 'upload/pepper/%s'
CLEDENTIAL_PATH = '<YOUR_CLEDENTIAL_PATH>'

def setup_cledential(cledential_path):
    '''
    set cledential
    '''
    # credential path
    keyPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), cledential_path)
    # credential setup
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyPath
    return True

def tranfer_gcp_storage(save_filepath, bucket_name=BUCKET_NAME, storage_path=STORAGE_PATH):
    '''
    transfer function: local to Google Cloud Storage
    ''' 

    # Instantiates a client
    storage_client = storage.Client()
    
    bucket = storage_client.get_bucket(bucket_name)

    save_filename = os.path.basename(save_filepath)   
    blob = bucket.blob(storage_path % (save_filename))
    
    blob.upload_from_filename(filename=save_filepath)
    return True
    
if __name__ == '__main__':
    # test code
    tranfer_gcp_storage('../flask_client/sweetsBag2_000001.jpg')
