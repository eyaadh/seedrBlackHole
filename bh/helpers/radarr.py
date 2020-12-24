import os
import logging
import json
import aiohttp
import urllib
from bh.helpers import Common


class RadarrProcessor:
    def __init__(self):
        self.web_dav = Common().radarr_url

    async def search_movie(self, search_term: str):
        endpoint = f"{self.web_dav}/api/movie/" \
                   f"lookup?term={urllib.parse.quote(search_term)}&apikey={Common().radarr_api_key}"
        async with aiohttp.ClientSession() as radarr_session:
            async with radarr_session.get(url=endpoint) as resp:
                try:
                    logging.info(await resp.text())
                    return json.loads(await resp.text())
                except Exception as e:
                    logging.error(e)
                    return None

    async def search_movie_imdb(self, imdb_id: str):
        endpoint = f"{self.web_dav}/api/movie/lookup/imdb?apikey={Common().radarr_api_key}"
        payload = {
            "imdbId": imdb_id,
        }
        async with aiohttp.ClientSession() as radarr_session:
            async with radarr_session.get(url=endpoint, params=payload) as resp:
                try:
                    logging.info(await resp.text())
                    return json.loads(await resp.text())
                except Exception as e:
                    logging.error(e)
                    return None

    async def add_movie(self, imdb_id: str):
        radarr_s_res = await self.search_movie_imdb(imdb_id)
        endpoint = f"{self.web_dav}/api/movie?apikey={Common().radarr_api_key}"
        m_path = os.path.join(Common().radarr_root_path, radarr_s_res['title'])
        payload = {
            "title": radarr_s_res['title'],
            "qualityProfileId": 0,
            "titleSlug": radarr_s_res['titleSlug'],
            "images": radarr_s_res['images'],
            "tmdbId": radarr_s_res['tmdbId'],
            "profileId": 3,
            "year": int(radarr_s_res['year']),
            "path": m_path,
            "monitored": True,
            "addOptions": {
                "searchForMovie": True
            }
        }

        payload = json.dumps(payload)

        async with aiohttp.ClientSession() as radarr_session:
            async with radarr_session.post(url=endpoint, data=payload) as resp:
                logging.info(await resp.text())
                print("Bingo")
                return json.loads(await resp.text())
