from cmd import Cmd

import spotipy
import spotipy.util
import lyricsgenius

from utils import *

class App(Cmd):

	'''Command-line application class'''

	spotify = {'USERNAME': '', 'CLIENT_ID': '', 'CLIENT_SECRET': '', 'REDIRECT_URI': ''}				#for Spotify attributes
	spotify_api = None																					#for Spotify API object

	lyrics_genius = {'TOKEN': ''}																		#for Lyrics Genius attributes
	lyrics_genius_api = None																			#for Lyrics Genius API object


	def do_SET(self, arg):
		'''
Use: SET <APP> <VAR>

Command dedicated to set the variables to initiate an application.

Spotify provides you:
	username (found in your personal account profile),
	client id (dashboard),
	client secret (dashboard),
	redirect uri (you must set in your app dashboard).

While Lyrics Genius provides you a token for it.

Parameters:

	APP:
		SPOTIFY
		LYRICS_GENIUS
	VAR:
		USERNAME (for Spotify)
		CLIENT_ID (for Spotify)
		CLIENT_SECRET (for Spotify)
		REDIRECT_URI (for Spotify)
		TOKEN (for Lyrics Genius)
		'''
		arg = arg.strip().split()																		#split arg string by spaces
		if check_arguments_number(arg, min = 3, max = 3) == -1:											#check number of arguments
			return																						#return if not correct

		if arg[0] == 'SPOTIFY':																			#if first argument is 'SPOTIFY'
			if arg[1] in list(self.spotify.keys()):														#if second argument is in spotify keys
				self.spotify[arg[1]] = arg[2]															#set spotify attribute
				print('Spotify', arg[1].capitalize().replace('_', ' '), '=', "'"+self.spotify[arg[1]]+"'", end = '\n\n')
			else:
				print('Invalid argument:', arg[1], end = '\n\n')										#else log error and return

		elif arg[0] == 'LYRICS_GENIUS':																	#else if first argument is 'LYRICS_GENIUS'
			if arg[1] == 'TOKEN':																		#if seconf argument is 'Token'
				self.lyrics_genius['TOKEN'] = arg[2]													#set lyrics_genius attribute
				print('Lyrics Genius Token =', "'"+self.lyrics_genius['TOKEN']+"'", end = '\n\n')
			else:
				print('Invalid argument:', arg[1], end = '\n\n')										#else log error and return

		else:
			print('Invalid argument:', arg[0], end = '\n\n')											#if invalid first argumernt, log error and return


	def do_INIT_SESSION(self, arg):
		'''
Use: INIT_SESSION <FILE> (optional)

Dedicated to initiate session. To do such, you must have all variables
setted to a valid string value. You can do that using the SET command
or passing a file containing your personal data as a optional argument.

For Spotify, you must contain have:
	
	username
	client_id
	client_secret
	redirect_uri

For Lyrics Genius, only your token.

Parameters:

	FILE:
		A .txt file path
		'''
		arg = arg.strip().split()																		#split arg string by spaces
		if check_arguments_number(arg, min = 0, max = 1) == -1:											#check number of arguments
			return																						#return if not correct

		if len(arg) == 1:																				#if provided two arguments:
			result = txt_to_list(arg[0])																#get file data
			if result == -1:
				return 																					#if failed, log error and return
			self.spotify = dict(zip(self.spotify.keys(), result[0]))									#else, set spotify attributes
			self.lyrics_genius['TOKEN'] = result[1]														#and lyrics genius attribute

		for i in self.spotify.items():																	#check if there are empty spotify attributes
			if i[1] == '':
				print('Spotify', i[0], 'not specified', end = '\n\n') 									#in the case, log error and return
				return

		for i in self.lyrics_genius.items():															#check if there are empty lyrics genius attributes
			if i[1] == '':
				print('Lyrics Genius', i[0], 'not specified', end = '\n\n')								#in the case, log error and return
				return																				

		try:																							#try to get spotify token
			token = spotipy.util.prompt_for_user_token(self.spotify['USERNAME'],
											   		   scope = None,
											   		   client_id = self.spotify['CLIENT_ID'],
											   		   client_secret = self.spotify['CLIENT_SECRET'],
											   		   redirect_uri = self.spotify['REDIRECT_URI'])
		except:
			try:
				os.remove(f".cache-{self.spotify['USERNAME']}")
				token = spotipy.util.prompt_for_user_token(self.spotify['USERNAME'],
												   		   scope = None,
												   		   client_id = self.spotify['CLIENT_ID'],
												   		   client_secret = self.spotify['CLIENT_SECRET'],
												   		   redirect_uri = self.spotify['REDIRECT_URI'])
			except:
				print("Couldn't initiate Spotify application. Please, try again", end = '\n\n')			#if failed, log error and return
				return

		self.spotify_api = spotipy.Spotify(auth = token)												#define spotify API object
		self.lyrics_genius_api = lyricsgenius.Genius(self.lyrics_genius['TOKEN'])						#define lyrics Genius API object
		print('Running session', end = '\n\n')


	def do_CLOSE_SESSION(self, arg):
		'''
Use: CLOSE_SESSION

Dedicated to stop running application.
		'''
		arg = arg.strip().split()																		#split arg string by spaces
		if check_arguments_number(arg, max = 0) == -1:													#check number of arguments
			return																						#return if not correct

		if self.spotify_api == None:																	#if spotify API object not defined
			print('No Spotify session currently running', end = '\n\n')									#log error and return
		else:
			self.spotify_api = None																		#else set spotify API object to none
			print('Stopped Spotify session', end = '\n\n')

		if self.lyrics_genius_api == None:																#if lyrics genius API object is none
			print('No Lyrics Genius session currently running', end = '\n\n')							#log error and return
		else:
			self.lyrics_genius_api = None 																#else set lyrics genius API object to none
			print('Stopped Lyrics Genius session', end = '\n\n')


	def do_SPOTIFY(self, arg):
		'''
Use: SPOTIFY <VAR>

Shows Spotify app variable.

Parameters:
	
	VAR:
		USERNAME
		CLIENT_ID
		CLIENT_SECRET
		REDIRECT_URI
		'''
		arg = arg.strip().split()																		#split arg string by spaces
		if check_arguments_number(arg, min = 1, max = 2) == -1:											#check number of arguments
			return																						#return if not correct

		if arg[0] in list(self.spotify.keys()):															#if second argument is in spotify keys
			print('Spotify', arg[0].capitalize().replace('_', ' '), '=', "'"+self.spotify[arg[0]]+"'", end = '\n\n')	#shows attribute
		else:
			print('Invalid argument:', arg[1], end = '\n\n')											#if invalid first argumernt, log error and return


	def do_LYRICS_GENIUS(self, arg):
		'''
Use: LYRICS_GENIUS <VAR>

Shows Lyrics Genius app variable.

Parameters:
	
	VAR:
		TOKEN
		'''
		arg = arg.strip().split()																		#split arg string by spaces
		if check_arguments_number(arg, min = 1, max = 2) == -1:											#check number of arguments
			return																						#return if not correct

		if arg[0] in list(self.lyrics_genius.keys()):													#if second argument is in lyrics genius keys
			print('Lyrics Genius', arg[0].capitalize().replace('_', ' '), '=', "'"+self.lyrics_genius[arg[0]]+"'", end = '\n\n')	#shows attribute
		else:
			print('Invalid argument:', arg[1], end = '\n\n')											#if invalid first argumernt, log error and return


	def do_GET(self, arg):
'''
Use: GET <PARAMETER1> <PATAMETER2>, <PARAMETER3> (optional)

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
			ARTIST
'''
		arg = arg.strip().split()																		#split arg string by spaces
		if check_arguments_number(arg, min = 2) == -1:													#check number of arguments
			return																						#return if not correct

		if arg[0] == 'ARTIST':																			#if first argument is 'ARTIST_ALBUMS'

			if self.spotify_api == None:																#if spotify API not running
				print('Spotify API session not running', end = '\n\n')									#log error and return
				return
			artist = ' '.join(arg[2:])																	#join last arguments in case of not sigle word artist

			if arg[1] == 'ALBUMS':
				albums = get_artist_albums(artist, self.spotify_api)									#get albums

				if albums == -1:																		#if failed
					print('Artist not found', end = '\n\n')												#log error and return
					return
				print('\n' + artist.capitalize() + ' albums:', end = '\n\n')							#else print table with requested content
				print_table(albums)

			elif arg[1] == 'TOP_TRACKS':
				top_tracks = get_artist_top_tracks(artist, self.spotify_api)							#get top tracks

				if top_tracks == -1:																	#if failed
					print('Artist not found', end = '\n\n')												#log error and return
					return
				print('\n' + artist.capitalize() + ' top tracks:', end = '\n\n')						#else print table with requested content
				print_table(top_tracks)

			else:
				print('Invalid argument:', arg[1], end = '\n\n')										#if invalid first argumernt, log error and return

		elif arg[0] == 'ALBUM':

			if self.spotify_api == None:																#if spotify API not running
				print('Spotify API session not running', end = '\n\n')									#log error and return
				return
			album = ' '.join(arg[2:])																	#join last arguments in case of not sigle word artist

			if arg[1] == 'TRACKLIST':
				tracklist, artist = get_album_tracklist(album, self.spotify_api)						#get tracklist and artist

				if tracklist == -1:																		#if failed
					print('Album not found', end = '\n\n')												#log error and return
					return	
				print('\n' + album.capitalize(), 'by', artist.capitalize(), 'tracklist:', end = '\n\n')	#else print table with requested content
				print_table(tracklist)

			else:
				print('Invalid argument:', arg[1], end = '\n\n')										#if invalid first argumernt, log error and return

		elif arg[0] == 'SONG':

			if self.lyrics_genius_api == None:															#if spotify API not running
				print('Lyrics Genius API session not running', end = '\n\n')							#log error and return
				return
			
			if len(' '.join(arg[2:]).split(',')) == 2:													#if composted argument
				song, artist = ' '.join(arg[2:]).split(',')												#separate in song and artist
				song, artist = song.strip().capitalize(), artist.strip().capitalize()

			else:
				song, artist = ' '.join(arg[2:]), ''													#else set empty artist

			if arg[1] == 'LYRICS':
				song_lyrics, artist = get_song_lyrics(song, artist, self.lyrics_genius_api)				#get tracklist and artist

				if song_lyrics == -1:																	#if failed
					return																				#return	
				print('\n' + song.capitalize(), 'by', artist.capitalize(), 'lyrics:', end = '\n\n')		#else print table with requested content
				print_table(song_lyrics.split('\n'))

		else:
			print('Invalid argument:', arg[1], end = '\n\n')											#if invalid first argumernt, log error and return


	def emptyline(self):
		pass 																							#if no command was passed, do nothing
