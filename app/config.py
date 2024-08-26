from os import getenv as org_getenv
from dotenv import load_dotenv

load_dotenv()

def getenv(key:str):
    value = org_getenv(key)
    if value is None:
        raise KeyError(f"Key {key} was not found in file .env")
    return value

class ConfigRequest():
    request_url = getenv('request_url')
    request_headers = {
        header.split(':')[0] : header.split(':')[1][1:-1]
        for header in getenv('request_headers').split('-|-')
    }
    regex_find_url = getenv('regex_find_url')
    regex_find_music_url = getenv('regex_find_music_url')
    request_timeout = int(getenv('request_timeout'))


class ConfigFlask():
    port = getenv('flask__port')
    limit = int(getenv("limit"))
    limit_check = int(getenv("limit_check"))


class ConfigApp():
    log_file = getenv('log_file')