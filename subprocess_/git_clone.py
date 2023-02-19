import subprocess

from _resources import test_folder_file

test_folder, test_file = test_folder_file()
test_file.unlink()

cmd_list = ['git', 'clone', 'https://github.com/CheeseCake87/Test-Private-Repo.git', test_folder]
cmd_str = f'git clone https://github.com/CheeseCake87/Test-Private-Repo.git {test_folder}'

process = subprocess.run(
    cmd_list
)
