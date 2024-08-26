import logging
from flask import Flask

from app.config import ConfigFlask, ConfigApp

config_flask = ConfigFlask()
config_app = ConfigApp()

app = Flask(__name__, '/')


formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(config_app.log_file, mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)
app.logger.setLevel(logging.DEBUG)

logger = app.logger

from app.routes import *