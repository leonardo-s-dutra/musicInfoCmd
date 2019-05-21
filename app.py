from cmd import Cmd

import spotipy
import spotipy.util
import lyricsgenius

from music_info_utils import *

class App(Cmd):

	'''Command-line application class'''

	credentials = {'USERNAME': '', 'ID': '', 'SECRET': '',											#credentials for running
				   'URI': '', 'TOKEN': ''}															#a session

	spotify_api = None																				#Spotify API object
	genius_api = None																				#Lyrics Genius API object

	def __init__(self, file=''):
		
		super(App, self).__init__()

		if file:

			credentials = txt_to_list(file)															#get file data
			if not credentials:
				return

			self.credentials = dict(zip(self.credentials.keys(), credentials))						#else, sets credentials from file

			for i in self.credentials.items():														#check if there are any empty credential
				if i[1] == '':
					print(i[0], 'not specified'+'\n')												#in this case, log error and return
					return																		

			try:																					#try to get spotify token
				token = spotipy.util.prompt_for_user_token(self.credentials['USERNAME'],
												   		   scope = None,
												   		   client_id = self.credentials['ID'],
												   		   client_secret = self.credentials['SECRET'],
												   		   redirect_uri = self.credentials['URI'])
			except:
				try:
					os.remove(f".cache-{self.credentials['USERNAME']}")
					token = spotipy.util.prompt_for_user_token(self.credentials['USERNAME'],
													   		   scope = None,
													   		   client_id = self.credentials['ID'],
													   		   client_secret = self.credentials['SECRET'],
													   		   redirect_uri = self.credentials['URI'])
				except Exception as e:
					print('\n'+e+'\n')																#if failed, log error and return
					return

			self.spotify_api = spotipy.Spotify(auth = token)										#define spotify API object
			self.genius_api = lyricsgenius.Genius(self.credentials['TOKEN'])						#define lyrics Genius API object


	def do_GET(self, arg):
		'''
Use: GET <PARAMETER1> <PATAMETER2>

Dedicated to show general information about an artist,
album or song.

Parameters:

	PARAMETER1:
		ARTIST:
			ALBUMS
			TOP_TRACKS		
		ALBUM:
			TRACKLIST
		SONG:
			LYRICS
		'''
		arg = arg.strip().split()																#split arg string by spaces
		if check_arguments_number(arg, min=2) == False:											#check number of arguments
			return																				#return if not correct

		if arg[0] == 'ARTIST':																	#if first argument is 'ARTIST_ALBUMS'

			if self.spotify_api == None:														#if spotify API not running
				print('Spotify API session not running'+'\n')									#log error and return
				return

			artist = ' '.join(arg[2:])															#join last arguments in case of not sigle word artist

			if arg[1] == 'ALBUMS':
				albums = get_artist_albums(artist, self.spotify_api)							#get albums
				if albums == -1:																#if failed
					print('Artist not found'+'\n')												#log error and return
					return
				print('\n'+artist.capitalize() + ' albums:'+'\n')								#else print table with requested content
				print_table(albums)

			elif arg[1] == 'TOP_TRACKS':
				top_tracks = get_artist_top_tracks(artist, self.spotify_api)					#get top tracks
				if top_tracks == -1:															#if failed
					print('Artist not found'+'\n')												#log error and return
					return
				print('\n'+artist.capitalize() + ' top tracks:'+'\n')							#else print table with requested content
				print_table(top_tracks)

			else:
				print('Invalid argument:', arg[1]+'\n')											#if invalid first argumernt, log error and return

		elif arg[0] == 'TRACKLIST':

			if self.spotify_api == None:														#if spotify API not running
				print('Spotify API session not running'+'\n')									#log error and return
				return
			
			album = ' '.join(arg[1:])															#join last arguments in case of not sigle word artist
			tracklist, artist = get_album_tracklist(album, self.spotify_api)					#get tracklist and artist

			if tracklist == -1:																	#if failed
				print('Album not found'+'\n')													#log error and return
				return	
			print('\n'+album.capitalize(), 'by', \
				  artist.capitalize(), 'tracklist:'+'\n')										#else print table with requested content
			print_table(tracklist)

		elif arg[0] == 'SONG':

			if self.genius_api == None:															#if spotify API not running
				print('Lyrics Genius API session not running'+'\n')								#log error and return
				return
			
			if len(' '.join(arg[2:]).split(',')) == 2:											#if composted argument
				song, artist = ' '.join(arg[2:]).split(',')										#separate in song and artist
				song, artist = song.strip().capitalize(), artist.strip().capitalize()

			else:
				song, artist = ' '.join(arg[2:]), ''											#else set empty artist

			if arg[1] == 'LYRICS':
				song_lyrics, artist = get_song_lyrics(song, artist, self.genius_api)			#get tracklist and artist
				if song_lyrics == -1:															#if failed
					return																		#return	
				print('\n'+song.capitalize(), 'by', artist.capitalize(), 'lyrics:'+'\n')		#else print table with requested content
				print_table(song_lyrics.split('\n'))

		else:
			print('Invalid argument:', arg[1]+'\n')												#if invalid first argumernt, log error and return
