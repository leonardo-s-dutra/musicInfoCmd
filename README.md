# MusicInfoCmd

A Python application for music information gathering via command-line based on Spotify and Lyrics Genius API's.

## Credentials

This app uses spotify and Lyrics Genius API's to provide information.

To get access, you need to provide credentials made by creating a spotify app at https://developer.spotify.com/.

For lyrics genius, you need to generate a token at https://docs.genius.com/#/getting-started-h1

## Getting access

When you run musicinfo.py, you need to provide a -f argument which is a text file containing your credentials. The file must contain:

username
client_id
client_secret
redirect_uri
token

In this exact order.

## Usage

With this app, you can get information from spotify with the command GET, which gives you parameters such:

* ARTIST
     * ALBUMS
     * TOP_TRACKS

* ALBUM
     * TRACKLIST
* SONG
     * LYRICS

You can also get your credential with the commands:

* SPOTIFY
    * USERNAME
    * ID
    * SECRET
    * URI
* LYRICS_GENIUS
    * TOKEN

Getting lyrics is the only resource used from Lyrics Genius API.  
  
If you have any doupt, check the help command or contact me ;)
