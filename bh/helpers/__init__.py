import base64
import configparser


class Common:
    def __init__(self):
        self.app_config = configparser.ConfigParser()
        self.app_config_file = "bh/working_dir/config.ini"
        self.app_config.read(self.app_config_file)
        self.working_dir = "bh/working_dir/"

        self.sonarr_torrent_location = self.app_config.get("sonarr", "torrent_loc")
        self.sonarr_watch_folder = self.app_config.get("sonarr", "watch_folder")

        self.seedr_username = self.app_config.get("seedr", "username")
        self.seedr_pwd = base64.b64decode(self.app_config.get("seedr", "password")).decode("utf-8")
