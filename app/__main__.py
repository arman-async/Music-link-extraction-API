import sys
from music_api.routes import *

if __name__ == "__main__":
    try:
        app.run('localhost', 9095, debug=True)
    except InterruptedError:
        sys.exit()