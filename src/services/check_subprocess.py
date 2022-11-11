import subprocess

def check_subprocess():

    pytonProcess = subprocess.check_output("ps -ef | grep .py", shell=True).decode()
    pytonProcess = pytonProcess.split('\n')
    for process in pytonProcess:
        print(process)

check_subprocess()