from pathlib import Path
from time import sleep

import pexpect


def header():
    print("=" * 80)


def footer():
    print("=" * 80)
    print(" " * 80)


def sub():
    print("-" * 80)


cwd = Path(__file__).parent
socket_file = Path(cwd, "supervisor.sock")
header()
print("Checking files...")
sub()
print("Current working directory:", cwd)
print("Socket file exists:", socket_file.exists())
footer()

header()
print("Starting supervisord...")
supervisord = pexpect.spawn('supervisord -c supervisord.conf', cwd=cwd)
print("Is supervisord alive?:", supervisord.isalive())
footer()

header()
print("Initial supervisord output...")
sub()
if isinstance(supervisord.before, bytes):
    print("Before\n", supervisord.before.decode().strip())
else:
    print("Before", None)

if isinstance(supervisord.after, bytes):
    print("After", supervisord.after.decode().strip())
else:
    print("After", None)
footer()

header()
print("While loop to check if process is alive and .sock file exists...")
while True:
    if supervisord.isalive():
        if socket_file.exists():
            print("supervisord socket file exists")
            break
    sleep(0.5)
footer()

header()
print("Starting supervisorctl...")
sub()
supervisorctl = pexpect.spawn('supervisorctl -c supervisord.conf', cwd=cwd)
supervisorctl.expect("supervisor> ")
print("Is supervisorctl alive and ready for sendline?:", supervisord.isalive())
footer()

header()
print("After supervisorctl.expect output...")
sub()
if isinstance(supervisorctl.before, bytes):
    print("supervisorctl Before\n", supervisorctl.before)
else:
    print("Before", None)
if isinstance(supervisorctl.after, bytes):
    print("supervisorctl After", supervisorctl.after)
else:
    print("After", None)
footer()

header()
print("Checking if processes are alive...")
sub()
print("supervisord alive?", supervisord.isalive())
print("supervisorctl alive?", supervisorctl.isalive())
footer()

header()
print("Checking again for output...")
sub()
if isinstance(supervisord.before, bytes):
    print("supervisord Before\n", supervisord.before.decode().strip())
else:
    print("supervisord Before", None)
if isinstance(supervisord.after, bytes):
    print("supervisord After", supervisord.after.decode().strip())
else:
    print("supervisord After", None)

if isinstance(supervisorctl.before, bytes):
    print("supervisorctl Before\n", supervisorctl.before.decode().strip())
else:
    print("supervisorctl Before", None)
if isinstance(supervisorctl.after, bytes):
    print("supervisorctl After", supervisorctl.after.decode().strip())
else:
    print("supervisorctl Before", None)
footer()

header()
print("Checking if processes are alive...")
sub()
print("supervisord alive?", supervisord.isalive())
print("supervisorctl alive?", supervisorctl.isalive())
footer()

header()
print("Start satellite...")
sub()
supervisorctl.sendline("start satellite")
supervisorctl.expect("supervisor> ")

if isinstance(supervisorctl.before, bytes):
    print("supervisorctl Before\n", supervisorctl.before.decode().strip())
else:
    print("supervisorctl Before", None)
if isinstance(supervisorctl.after, bytes):
    print("supervisorctl After", supervisorctl.after.decode().strip())
else:
    print("supervisorctl Before", None)

supervisorctl.sendline("status")
supervisorctl.expect("supervisor> ")

if isinstance(supervisorctl.before, bytes):
    print("supervisorctl Before\n", supervisorctl.before.decode().strip())
else:
    print("supervisorctl Before", None)
if isinstance(supervisorctl.after, bytes):
    print("supervisorctl After", supervisorctl.after.decode().strip())
else:
    print("supervisorctl Before", None)

footer()

header()
_ = input("Press enter to close...")
footer()

header()
print("Sending an exit command to supervisorctl and checking response...")
supervisorctl.sendline("exit")
footer()

header()
print("Waiting for supervisorctl to close...")
sub()
while True:
    if not supervisorctl.isalive():
        print("supervisorctl has stopped")
        break
    sleep(0.5)
footer()

header()
print("Checking what processes are alive...")
sub()
print("supervisord alive?", supervisord.isalive())
print("supervisorctl alive?", supervisorctl.isalive())
footer()

header()
print("Closing supervisord with Ctrl+C...")
supervisord.sendcontrol("c")
footer()

header()
print("Waiting for supervisord to close...")
sub()
while True:
    if not supervisord.isalive():
        print("supervisord has stopped")
        break
    sleep(0.5)
footer()

header()
print("Checking what processes are alive...")
sub()
print("supervisord alive?", supervisord.isalive())
print("supervisorctl alive?", supervisorctl.isalive())
footer()

if supervisord.isalive():
    header()
    print("Closing supervisord...")
    supervisord.close()
    footer()
