import os
import logging
from bh.helpers import Common
from bh.helpers.seedr_api import SeedrProcessor


class Cron:
    @staticmethod
    async def check_for_new_series():
        if len(os.listdir(Common().sonarr_torrent_location)) > 0:
            files = os.listdir(Common().sonarr_torrent_location)
            for file in files:
                tor_file = os.path.join(Common().sonarr_torrent_location, file)
                seedr_resp = await SeedrProcessor().add_file(tor_file)

                try:
                    if seedr_resp['code'] == 200:
                        logging.info(f"Grabbed Torrent File: {tor_file}")
                        if os.path.isfile(tor_file):
                            os.remove(tor_file)

                        await SeedrProcessor().wait_for_seedr_download(seedr_resp)
                    else:
                        logging.error(f"Error Grabbed Torrent File: {tor_file} - Error Code: {seedr_resp['code']} - "
                                      f"Error Description: {seedr_resp['error']}")
                        if os.path.isfile(tor_file):
                            os.remove(tor_file)
                except Exception as e:
                    logging.error(f"Error Grabbed Torrent File: {e}")
        else:
            logging.info("No New Series")
