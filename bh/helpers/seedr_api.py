import os
import json
import shutil
import asyncio
import aiohttp
import logging
import secrets
import zipfile
import aiofiles
import requests
import mimetypes
import humanfriendly as size
from bh.helpers import Common
from shutil import copyfile


class SeedrProcessor:
    def __init__(self):
        self.web_dav = "https://www.seedr.cc/rest"

    async def add_url(self, url: str, link_type: str):
        async with aiohttp.ClientSession() as seedr_session:
            endpoint = f"{self.web_dav}/torrent/magnet" if link_type == "magnet" else f"{self.web_dav}/torrent/url"
            data = {"magnet": url} if link_type == "magnet" else {"torrent_url": url}
            async with seedr_session.post(
                    url=endpoint,
                    data=data,
                    auth=aiohttp.BasicAuth(
                        Common().seedr_username,
                        Common().seedr_pwd
                    )
            ) as resp:
                logging.info(await resp.text())
                return json.loads(await resp.text())

    async def add_file(self, file: str):

        from requests.auth import HTTPBasicAuth
        data = {'torrent_file': (os.path.basename(file), open(file, 'rb'), mimetypes.guess_type(file)),
                'Content-Disposition': 'form-data; name="file"; filename="' + os.path.basename(file) + '"',
                'Content-Type': mimetypes.guess_type(file)}
        endpoint = f"{self.web_dav}/torrent/url"
        with requests.post(
                endpoint, files=data, auth=HTTPBasicAuth(Common().seedr_username, Common().seedr_pwd)) as resp:
            return json.loads(resp.text)

    async def get_torrent_details(self, torrent_id: str):
        async with aiohttp.ClientSession() as seedr_session:
            endpoint = f"{self.web_dav}/torrent/{torrent_id}"
            async with seedr_session.get(
                    url=endpoint,
                    auth=aiohttp.BasicAuth(
                        Common().seedr_username,
                        Common().seedr_pwd
                    )
            ) as resp:
                return json.loads(await resp.text())

    async def get_folder(self, folder_id: str):
        async with aiohttp.ClientSession() as seedr_session:
            endpoint = f"{self.web_dav}/folder/{folder_id}"
            async with seedr_session.get(
                    url=endpoint,
                    auth=aiohttp.BasicAuth(
                        Common().seedr_username,
                        Common().seedr_pwd
                    )
            ) as resp:
                return json.loads(await resp.text())

    async def delete_folder(self, folder_id: str):
        async with aiohttp.ClientSession() as seedr_session:
            endpoint = f"{self.web_dav}/folder/{folder_id}"
            async with seedr_session.delete(
                    url=endpoint,
                    auth=aiohttp.BasicAuth(
                        Common().seedr_username,
                        Common().seedr_pwd
                    )
            ) as resp:
                return json.loads(await resp.text())

    async def download_file(self, file_id: str, file_name: str):
        endpoint = f"{self.web_dav}/file/{file_id}"

        temp_dir = os.path.join(Common().working_dir, secrets.token_hex(2))
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        temp_file = os.path.join(temp_dir, file_name)

        async with aiohttp.ClientSession() as seedr_session:
            async with seedr_session.get(
                    url=endpoint,
                    auth=aiohttp.BasicAuth(
                        Common().seedr_username,
                        Common().seedr_pwd
                    )
            ) as resp:
                async with aiofiles.open(temp_file, mode="wb") as fd:
                    downloaded = 0
                    async for chunk in resp.content.iter_any():
                        downloaded += len(chunk)
                        await fd.write(chunk)
                        logging.info(f"Downloading File: Progress - {size.format_size(downloaded, binary=True)} "
                                     f"- File: {temp_file}")

        # await UploadProcessor().upload_files(temp_file, ack_message, "other")

    async def download_folder(self, folder_id: str, upload_type: str):
        endpoint = f"{self.web_dav}/folder/{folder_id}/download"

        temp_dir = os.path.join(Common().working_dir, secrets.token_hex(2))
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        folder_details = await self.get_folder(folder_id)
        dl_folder_name = f"{folder_details['name']}.zip"
        dl_compressed_file = os.path.join(temp_dir, dl_folder_name)

        if not os.path.exists(os.path.dirname(dl_compressed_file)):
            os.mkdir(os.path.dirname(dl_compressed_file))

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1200)) as seedr_session:
            async with seedr_session.get(
                    url=endpoint,
                    auth=aiohttp.BasicAuth(
                        Common().seedr_username,
                        Common().seedr_pwd
                    )
            ) as resp:
                async with aiofiles.open(dl_compressed_file, mode="wb") as fd:
                    downloaded = 0

                    async for chunk in resp.content.iter_any():
                        downloaded += len(chunk)
                        await fd.write(chunk)
                        logging.info(f"Downloading: Progress - {size.format_size(downloaded, binary=True)} "
                                     f"File: {dl_compressed_file}")

        if upload_type == "compressed":
            await self.uncompress_upload(dl_compressed_file)

    @staticmethod
    async def uncompress_upload(compressed_file: str):
        zf = zipfile.ZipFile(compressed_file)
        parent_path = os.path.dirname(compressed_file)
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_files = []
        extracted_size = 0

        for file in zf.infolist():
            extracted_size += file.file_size
            extracted_progress = extracted_size * 100 / uncompress_size

            logging.info(f"Extracting file: {int(extracted_progress)} %  {compressed_file}")

            extracted_files.append(zf.extract(file, path=parent_path))
        zf.close()

        x = 0
        for file in extracted_files:
            x = x + 1
            if (mimetypes.guess_type(file)[0].split('/')[0]).lower() == 'video':
                dst_file = os.path.join(Common().sonarr_watch_folder, os.path.basename(file))
                copyfile(file, dst_file)

        if os.path.exists(parent_path):
            try:
                shutil.rmtree(parent_path)
            except Exception as e:
                logging.error(str(e))

    @staticmethod
    async def wait_for_seedr_download(tr_process):
        try:
            tr_progress = await SeedrProcessor().get_torrent_details(tr_process["user_torrent_id"])
            while True:
                if tr_progress["progress"] < 100:
                    tr_progress = await SeedrProcessor().get_torrent_details(tr_process["user_torrent_id"])
                    await asyncio.sleep(1)
                    logging.info(f"Seedr Progress: {tr_process['title']} "
                                 f"Progress: {tr_progress['progress']}% | "
                                 f"Size: {size.format_size(tr_progress['size'], binary=True)}")
                else:
                    tr_progress = await SeedrProcessor().get_torrent_details(tr_process["user_torrent_id"])
                    await SeedrProcessor().download_folder(tr_progress['folder_created'], "compressed")
                    break
        except Exception as e:
            logging.error(e)
