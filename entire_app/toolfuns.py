
import hashlib

def md5(some_str):
    return str(hashlib.md5(some_str.encode()).hexdigest())