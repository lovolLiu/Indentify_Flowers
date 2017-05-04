# -*- coding:utf-8 -*-
import os


def upload(dir_path, uploaded_file):
    try:
        filename = uploaded_file.filename
        path = dir_path + "/" + filename
        uploaded_file.save(path)
        return {'status': 'ok'}
    except Exception, e:
        print e
        return {'status': 'error'}
