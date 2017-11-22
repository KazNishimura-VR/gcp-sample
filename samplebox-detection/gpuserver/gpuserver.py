#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

import gpupredict as gpupredict
import transsto as transsto

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
API_KEY = 'YOUR_API_KEY'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='api gateway', name='test')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    '''
    upload API
    '''
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    remote_ip = request.remote_addr
    
    # post
    if request.method == 'POST':

        # check API Key
        api_key = request.headers.get('Bearer')
        if api_key != API_KEY:
             result = {'error': 'API key error'}
             print ("%s %s" % (remote_ip, 'API key error'))
             return jsonify(result)

        # check File
        if 'file' not in request.files:
            result = {'error': 'no upload file found'}
            print ("%s %s" % (remote_ip, 'no upload file found'))
            return jsonify(result)

        # upload params
        upload_file = request.files['file']
        upload_id = get_randid()
        save_filename = "%s_%s_%s" % (timestamp, upload_id, secure_filename(upload_file.filename))
        upload_path = "uploads/%s" % save_filename
        xml_path = "results/%s.xml" % os.path.splitext(save_filename)[0]

        # check and create floder
        if (os.path.exists('uploads') == False):
            os.mkdir('uploads')
        if (os.path.exists('results') == False):
            os.mkdir('results')
           
        upload_file.save(upload_path)

        # API return
        prediction_result = attach_upload(upload_path)

        # save to cloud storage (image)
        if(os.path.exists(upload_path)):
            transsto.tranfer_gcp_storage(upload_path)
            os.remove(upload_path)

        # save to cloud storage (resultxml)
        if(os.path.exists(xml_path)):
            transsto.tranfer_gcp_storage(xml_path)
            os.remove(xml_path)
        
        return jsonify(prediction_result)

    # other method
    else:
        result = {'error': 'method error'}
        return jsonify(result)

def attach_upload(upload_path):
    '''
    impliment prediction code
    '''
    prediction_result = {}
    
    #print(upload_path)
    gpupredict.process_image(upload_path)
    
    return gpupredict.process_image(upload_path)
    
def get_randid():
    '''
    generate random id
    '''
    return  "".join([random.choice('abcdefghijklmnopqrstuvwxyz') for x in range(10)])

if __name__ == '__main__':
    transsto.setup_cledential('YOUR_CLEDENTIAL_PATH')
    app.debug = True
    app.run(host='0.0.0.0')
