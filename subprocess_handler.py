import subprocess
import os


def run_subprocess(command, cwd=os.curdir):
    pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    std_out, std_err = pipes.communicate()
    std_out, std_err = str(std_out, encoding='utf-8'), str(std_err, encoding='utf-8')
    return std_out, std_err, pipes.returncode
