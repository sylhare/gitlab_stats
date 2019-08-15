import json
import re
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import requests

import tests


class MockGitlabServer(BaseHTTPRequestHandler):
    PIPELINE = re.compile(r'pipelines')
    PROJECTS = re.compile(r'projects')
    PER_PAGE = re.compile(r'per_page')
    THE_PROJECT = re.compile(r'4895805')
    THE_PIPELINE = re.compile(r'33409')

    def do_GET(self):
        """ Default get handler method of BaseHTTPRequestHandler """
        if self.headers['PRIVATE-TOKEN'] == 'wrong token':  # 004
            self.wrong_token_response()
        elif re.search(self.PIPELINE, self.path) and re.search(self.PER_PAGE, self.path):  # 013, 020
            self.send_all_pipeline()
        elif re.search(self.PROJECTS, self.path) and re.search(self.PER_PAGE, self.path):  # 011, 012
            self.send_all_projects()
        elif re.search(self.PIPELINE, self.path) and re.search(self.THE_PIPELINE, self.path):  # 013, 014, 021, 022
            self.send_pipeline()
        elif re.search(self.THE_PROJECT, self.path):  # 010, 015
            self.send_project()
        elif re.search(self.PROJECTS, self.path):  # 002
            self.default_answer()
        else:
            self.send_response(requests.codes.not_found)

    def wrong_token_response(self):
        self.send_response(requests.codes.not_found)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps([{}])
        self.wfile.write(response_content.encode('utf-8'))

    def default_answer(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps([{}])
        self.wfile.write(response_content.encode('utf-8'))

    def send_project(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PROJECT_INFO)
        self.wfile.write(response_content.encode('utf-8'))

    def send_pipeline(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PIPELINE_INFO)
        self.wfile.write(response_content.encode('utf-8'))

    def send_all_projects(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PROJECT_ALL)
        self.wfile.write(response_content.encode('utf-8'))

    def send_all_pipeline(self):
        self.send_response(requests.codes.ok)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        response_content = json.dumps(tests.PIPELINES_ALL)
        self.wfile.write(response_content.encode('utf-8'))


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port, server):
    mock_server = HTTPServer(('localhost', port), server)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
