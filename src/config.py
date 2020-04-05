from configparser import ConfigParser
from constant import SRC_PATH
from os import path

config_path = SRC_PATH + "/../config.ini"

config = ConfigParser()
if not path.exists(config_path):
    print("Creating config.ini in the root directory, fill in the fields and rerun")
    config.read(config_path)
    config.add_section("main")
    config.set("main", "client_id", "")
    config.set("main", "client_secret", "")
    config.set("main", "redirect_uri", "")
    config.set("main", "port", "")
    with open(config_path, "w") as f:
        config.write(f)
    exit()

config.read(config_path)
client_id = config.get("main", "client_id")
client_secret = config.get("main", "client_secret")
redirect_uri = config.get("main", "redirect_uri")
port = config.get("main", "port")
