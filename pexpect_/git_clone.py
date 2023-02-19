import pexpect

from _resources import test_folder_file

test_folder, test_file = test_folder_file()
test_file.unlink()

# https://github.com/Flask-Planet/flask-planet.org.git

cmd_list = ['git', 'clone', 'https://github.com/CheeseCake87/Test-Private-Repo.git', test_folder]
cmd_str = f'git clone https://github.com/CheeseCake87/Test-Private-Repo.git {test_folder}'

child = pexpect.spawn(cmd_str, timeout=5)

output_lines = []

child.expect(['Username', pexpect.EOF])
if child.isalive():
    child.close()

if isinstance(child.before, bytes):
    output_lines.append(child.before.decode('utf-8'))
if isinstance(child.after, bytes):
    output_lines.append(child.after.decode('utf-8'))

for line in output_lines:
    print(line)
