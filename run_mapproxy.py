# -*- coding: utf-8 -*-
# Copyright (C) 2017 Piotr Pociask <http://gis-support.pl>
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

from mapproxy.wsgiapp import make_wsgi_app
from werkzeug.serving import run_with_reloader
from eventlet import wsgi
import eventlet
import os
import logging
import logging.handlers

#Configuration

HOST = '127.0.0.1'
PORT = 8080
LOG_FILENAME = 'mapproxy.log'
CONFIG_FILE = 'grodzisk.yaml'

def get_logger():
    """ Logger for events """
    logger = logging.getLogger('mapproxy_logger')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(get_full_path(LOG_FILENAME),
                                                   maxBytes=10*1024000, #MB
                                                   backupCount=5,
                                                   )
    logger.addHandler(handler)
    return logger

def get_full_path( file_name ):
    """ Full path to file in root folder """
    return os.path.join( os.path.dirname(os.path.abspath(__file__)), file_name)

def start_mapproxy(with_reloader=True, use_logger=True):
    """ Run wsgi server """
    app = make_wsgi_app( get_full_path(CONFIG_FILE) )
    def run_server():
        logger = get_logger() if use_logger else None
        wsgi.server(eventlet.listen((HOST, PORT)), app, log=logger)
    if with_reloader:
        run_with_reloader( run_server )
    else:
        run_server()

if __name__=='__main__':
    start_mapproxy()