import ast
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

        self.radarr_api_key = self.app_config.get("radarr", "api_key")
        self.radarr_url = self.app_config.get("radarr", "url")
        self.radarr_torrent_location = self.app_config.get("radarr", "torrent_loc")
        self.radarr_watch_folder = self.app_config.get("radarr", "watch_folder")
        self.radarr_root_path = self.app_config.get("radarr", "radarr_root")

        self.seedr_username = self.app_config.get("seedr", "username")
        self.seedr_pwd = base64.b64decode(self.app_config.get("seedr", "password")).decode("utf-8")

        self.tg_app_id = int(self.app_config.get("pyrogram", "api_id"))
        self.tg_api_key = self.app_config.get("pyrogram", "api_hash")

        self.bot_session = self.app_config.get("bot-configuration", "session")
        self.bot_api_key = self.app_config.get("bot-configuration", "api_key")
        self.bot_dustbin = int(self.app_config.get("bot-configuration", "dustbin"))
        self.app_sudo_users = ast.literal_eval(self.app_config.get('bot-configuration', 'sudo_users'))
