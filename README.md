# Seedr Black Hole
The project has been done with the mindset of creating a butler/bot to a Media Management Project for a VOD Service - where the application handles downloads and requests for Movies by the end users. 
The VOD service uses PLEX as the main client–server media player system. Radarr to assist with
search and manage Movies and Sonarr for TV series. Jackett to provide indexers for both Radarr and Sonarr.

Now let me explain where "Seedr Black Hole" fits in this mighty mixture of application suites:
- It acts as the torrent client (uses Seedr API) for both Sonarr and Radarr.
- Assist end users to search for movies over telegram and add them to Radarr in a much convenient method (inline results).

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
    
    ###