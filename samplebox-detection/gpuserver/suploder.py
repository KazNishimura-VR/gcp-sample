#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
API_KEY = 'YOUR_GPU_SERVER_KEY'

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
        save_filename = "%s_%s" % (timestamp, secure_filename(upload_file.filename))
        upload_path = "uploads/%s" % save_filename

        if (os.path.exists('uploads') == False):
            os.mkdir('uploads')
        upload_file.save(upload_path)

        # API return
        result = {'ok': 'uploaded %s' % (upload_file.filename), 'timestamp': timestamp}
        print ("%s uploaded %s" % (remote_ip, save_filename))

        return jsonify(result)

    # other method
    else:
        result = {'error': 'method error'}
        return jsonify(result)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
