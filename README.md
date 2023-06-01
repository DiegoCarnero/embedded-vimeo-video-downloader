# Embedded vimeo video downloader
Python program that lets you download embedded vimeo videos.

Many websites use vimeo as a hosting platform and them add custom controls to the video player, so this has the potential to be useful in many sites.
## Usage
1. On a web browser, access a web page with an embedded video.
2. Right-click > Inspect  to open Developer tools.
3. Go to the 'Network' tab and write `player` on the filter textbox.
4. Reload the page.
5. There should be:
    - an entry with a string of 8 numbers of type 'document'.
    - a `player.module.js` entry with that string of 8 numbers as 'Initiator'
6. Click the 'document' entry and go to the 'Response' tab.
7. Copy the contents of the 'Response' tab to the `response.html` file on this repository.
8. Launch the python script `vimeo_download.py`. The highest resolution version of the video will be downloaded

This method also allow you to download videos behind authentification pages and the usual 'Sorry.
Because of its privacy settings, this video cannot be played here.' error page.

## TODOs
- [ ] Allow user to specify a name for the downloaded video
- [ ] Allow user to select quality options
- [ ] Download video from url alone