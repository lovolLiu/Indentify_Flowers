# -*- coding:utf-8 -*-
from flask import render_template, request
from app import app
from services import upload
from flask import jsonify
import os

# get the current folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    dir_path = os.path.join(APP_ROOT, 'static/data')
    result = upload(dir_path, uploaded_file)
    return jsonify(result)
