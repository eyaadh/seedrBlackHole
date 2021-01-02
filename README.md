# Seedr Black Hole
The project has been done with the mindset of being an assistant to a Media management project for a VOD Service which
we like to call as Falcon. The VOD service uses PLEX as the main client–server media player system. Radarr to assist with
search, download, and manage Movies and Sonarr for TV series. Jackett to provide indexers for both Radarr and Sonarr.

Now let me explain you where "Seedr Black Hole" fits in this mighty mixture of application suites:
- It acts as the torrent client (uses Seedr API) for both Sonarr and Radarr.
- Assist end users to search for movies over telegram and add them to Radarr using its API.

## Installation and setup of Jackett, Sonarr & Radarr:
- Sonarr Installation can be found [here](https://sonarr.tv/#download):
- Radarr Installation can be found [here](https://radarr.video/#download).
- Jackett Installation can be found [here](https://github.com/Jackett/Jackett#installation-on-windows)
    ### Setting up of torrent client for both Sonarr & Radarr:
    - Go to Settings>Download Clinets> and select [+] button to add a new client.
    - From the options available select Torrent Blackhole.
    - Basically a torrent blackhole client puts .torrent files into a folder, to be picked up by an external tool. Will watch another folder to check for completed downloads.
    - Make sure that "Save Magnet Files" are unselected from options as you add the client as well "Read Only" option is unselected as we also want to import the files to their 
    respective directories rather than keeping it duplicate. \
      <i>Note: Make a note of Torrent Folder and Watch Folder as you would need them on the config.ini file for Seedr Black Hole. Here Torrent folder is to which Radarr/Sonarr will save the respective torrent file for Seedr Black Hole to grab and add start the process of downloading when
      there is a new torrent. Also make sure torrent watch folder is always empty unless it is a torrent file from Radarr/Sonarr. Watch folder is which Sonarr/Radarr will look for complete downloads to import them to library.</i>
