import hashlib


sha256 = hashlib.sha256


def get_sha256(name):
    return sha256(name.encode('utf-8')).hexdigest()
