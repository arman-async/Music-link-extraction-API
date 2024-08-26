import sys
from app import app
app = app
if __name__ == "__main__":
    try:
        app.run('localhost', 5000, debug=True)
    except InterruptedError:
        sys.exit()