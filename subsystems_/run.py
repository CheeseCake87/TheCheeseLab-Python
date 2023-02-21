import subprocess
from concurrent.futures import ThreadPoolExecutor


def supervisord():
    command = ('supervisord')
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.communicate()


with ThreadPoolExecutor(max_workers=8) as executor:
    future = executor.map(supervisord)
    future.result()
