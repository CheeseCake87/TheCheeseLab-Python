import logging
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pexpect

logging.basicConfig(level=logging.DEBUG)

CWD = Path.cwd()
SOCKET = Path.cwd() / 'supervisor.sock'


class Launcher:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)

    def start(self):
        self.supervisord = self.executor.submit(launch_supervisord)
        # self.supervisorctl = self.executor.submit(launch_supervisorctl)
        self.gunicorn = self.executor.submit(launch_gunicorn)

        self.supervisord_process = self.supervisord.result()
        # self.supervisorctl_process = self.supervisorctl.result()
        self.gunicorn_process = self.gunicorn.result()

    def __enter__(self):
        return self.start

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.supervisorctl_process.sendcontrol('c')
        # while True:
        #     if self.supervisorctl_process.isalive():
        #         time.sleep(1)
        #     else:
        #         break

        self.supervisord_process.sendcontrol('c')

        while True:
            if not SOCKET.exists():
                break
            time.sleep(1)

        exit()


def launch_supervisord():
    process = pexpect.spawn('venv/bin/supervisord', cwd=CWD)
    return process


def launch_supervisorctl():
    while True:
        if SOCKET.exists():
            break
        time.sleep(1)

    process = pexpect.spawn('venv/bin/supervisorctl', cwd=CWD)
    return process


def launch_gunicorn():
    gunicorn_config = Path.cwd() / 'gunicorn.conf.py'
    assert gunicorn_config.exists()

    process = subprocess.run(['venv/bin/gunicorn'], cwd=CWD, stdout=sys.stdout, stderr=sys.stderr)
    return process


with Launcher() as start:
    start()
