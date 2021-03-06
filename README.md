# Seedr Black Hole
The project has been done with the mindset of creating a butler/bot to a Media Management Project for a VOD Service - where the application handles downloads and requests for Movies by the end users. 
The VOD service uses PLEX as the main client–server media player system. Radarr to assist with
search and manage Movies and Sonarr for TV series. Jackett to provide indexers for both Radarr and Sonarr.

Now let me explain where "Seedr Black Hole" fits in this mighty mixture of application suites:
- It acts as the torrent client (uses Seedr API) for both Sonarr and Radarr.
- Assist end users to search for movies over telegram and add them to Radarr in a much convenient/interactive method (inline results).

<i>The whole Project was build based on Windows 10 and Python 3.8.1. It uses Pyrogram to communicate with Telegram.</i>

## Installation and setup of Jackett, Sonarr & Radarr:
- Sonarr Installation can be found [here](https://sonarr.tv/#download):
- Radarr Installation can be found [here](https://radarr.video/#download).
- Jackett Installation can be found [here](https://github.com/Jackett/Jackett#installation-on-windows)
    ### Setting up of torrent client for both Sonarr & Radarr:
    - Go to Settings>Download Clinets> and select [+] button to add a new client.
    - From the options available select Torrent Blackhole.
    - Basically a torrent blackhole client puts .torrent files into a folder, to be picked up by an external tool (in this case Seedr Black Hole). Will watch another folder to check for completed downloads.
    - Make sure that "Save Magnet Files" are unselected from options as you add the client as well "Read Only" option is unselected as we also want to import the files to their 
    respective directories rather than keeping it duplicate. \
      <i>Note: Make a note of Torrent Folder and Watch Folder as you would need them on the config.ini file for Seedr Black Hole.
      Also make sure torrent watch folder is always empty unless it is a torrent file from Radarr/Sonarr. Watch folder is which Sonarr/Radarr will look for complete downloads to import them to library.</i>
      
    ### Setting up indexers:
    - Once you have installed jackett you can enable/add the indexers of your choice.
    - Now go back to Sonarr/Radarr and perform the bellow steps.
    - Go to Settings>Indexers> and select [+] button to add a new indexer.
    - Give a name of your choosing, keep the rest at default and fill in the URL with details to Jackett host. For instance if you had installed jackett 
    on the same machine as Sonarr/Raddar: http://localhost:9117
    - And the API path to be set as /api/v2.0/indexers/all/results/torznab (this might be a hidden attribute, you need to have advance settings enable to see it).
    - Finally the API key from Jackett and press "Save"
  

Note: You can connect both Sonarr/Radarr to inform the bot and plex once a media is Grabbed (notify when available for download), on Download (when the media download is completed) by adding them under Settings>Connect, its 
recommended doing so since this would keep the whole project more personalized.

## Cloning & Run:
1. `git clone https://github.com/eyaadh/seedrBlackHole.git`, to clone the repository.
2. `cd seedrBlackHole`, to enter the directory.
3. `pip install -r requirements.txt`, to install rest of the dependencies/requirements.
4. Create a new `config.ini` in working_dir using the sample available at `bh/working_dir/config.ini.sample`.
5. Run with `python -m bh`, stop with <kbd>CTRL</kbd>+<kbd>C</kbd>.
> It is recommended to use [virtual environments](https://docs.python-guide.org/dev/virtualenvs/) while running the app, this is a good practice you can use at any of your python projects as virtualenv creates an isolated Python environment which is specific to your project.

### A brief on Config.ini:
```
[pyrogram]
# More info on API_ID and API_HASH can be found here: https://docs.pyrogram.org/intro/setup#api-keys
api_id =
api_hash =

[bot-configuration]
# More info on Bot API Key/token can be found here: https://core.telegram.org/bots#6-botfather
api_key =
session = falcon
# The chat ID for the group at which end users will be interacting with the telegram bot.
dustbin = -1001382246125
# The admin users who are allowed to accept the media requests that comes in.
sudo_users = [200344026,1234]

[plugins]
root = bh/telegram/plugins

[sonarr]
# Here the torrent location is the "Torrent Folder" from the black hole setup we did earlier and watch_folder is "Watch Folder" from the same step.
torrent_loc=
watch_folder=

[radarr]
# Here the torrent location is the "Torrent Folder" from the black hole setup we did earlier and watch_folder is "Watch Folder" from the same step.
# The API key for radarr can be found within Settings>General of Radarr.
api_key =
url =
torrent_loc=
watch_folder=
radarr_root=

[seedr]
# You know exactly what needs to be within here. For which ever stupid reason I didn't want the password which is in this configuration file to be plain 
# to read i.e. the application expects the base64 encoded value for the password to be within here. An easy online tool to encode base64 is https://www.base64encode.org/
username =
password =
```