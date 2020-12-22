import os
import asyncio
import logging
from bh.helpers import Common
from bh.helpers.seedr_api import SeedrProcessor


class Cron:
    @staticmethod
    async def check_for_new_dl():
        if len(os.listdir(Common().sonarr_torrent_location)) > 0:
            await Cron().new_torrents_found("series")

        if len(os.listdir(Common().radarr_torrent_location)) > 0:
            await Cron().new_torrents_found("movies")

    @staticmethod
    async def new_torrents_found(tor_type: str):
        location = Common().sonarr_torrent_location if tor_type == "series" else Common().radarr_torrent_location
        files = os.listdir(location)
        for file in files:
            tor_file = os.path.join(location, file)
            seedr_resp = await SeedrProcessor().add_file(tor_file)

            try:
                if seedr_resp['code'] == 200:
                    logging.info(f"Grabbed Torrent File: {tor_file}")
                    if os.path.isfile(tor_file):
                        os.remove(tor_file)

                    await SeedrProcessor().wait_for_seedr_download(seedr_resp, tor_type)
                else:
                    logging.error(f"Error Grabbed Torrent File: {tor_file} - Error Code: {seedr_resp['code']} - "
                                  f"Error Description: {seedr_resp['error']}")
                    if os.path.isfile(tor_file):
                        os.remove(tor_file)
            except Exception as e:
                logging.error(f"Error Grabbed Torrent File: {e}")

            await asyncio.sleep(10)
