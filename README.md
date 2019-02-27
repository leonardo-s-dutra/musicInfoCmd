# musicInfoCmd

A Python application for music information gathering via command-line based on Spotify and Lyrics Genius API's.

## Credentials

This app uses spotify and Lyrics Genius API's to provide information.

To get access, you need to provide credentials made by creating a spotify app at https://developer.spotify.com/.

For lyrics genius, you need to generate a token at https://docs.genius.com/#/getting-started-h1

## Getting access

Before running any command, you need to run INIT_SESSION, which will check for your credentials. You should set them using the SET command followed by the credential and its value or run INIT_SESSION giving a file containing the credentials as a optional argument.

The file should look like this:

username  
client ID  
client secret  
redirect URL  
Token  

In this exact order.  

You can also use the CLOSE_SESSION command to change variables or something like that.

## Usage

With this app, you can get information from spotify with commands like GET, which gives you parameters such:

* ARTIST
     * ALBUMS
     * TOP_TRACKS

* ALBUM
     * TRACKLIST
* SONG
     * LYRICS
     * ARTIST
  
Getting lyrics is the only resource used from Lyrics Genius API.  
  
If you have any doupt, check the help command or contact me ;)
