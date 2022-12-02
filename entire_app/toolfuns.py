
import hashlib
import pathlib

def md5(some_str):
    return str(hashlib.md5(some_str.encode()).hexdigest())
    
def ffile(file_path):
    return pathlib.Path(file_path)