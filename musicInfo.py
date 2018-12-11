from cmd import Cmd

import spotipy
import spotipy.util
import lyricsgenius

from utils import *

class App(Cmd):

	'''Command-line application class'''

	spotify = {'USERNAME': '', 'CLIENT_ID': '', 'CLIENT_SECRET': '', 'REDIRECT_URI': ''}			#for Spotify attributes
	spotify_api = None																				#for Spotify API object

	lyrics_genius = {'TOKEN': ''}																	#for Lyrics Genius attributes
	lyrics_genius_api = None																		#for Lyrics Genius API object


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
		arg = arg.strip().split()														#Separate arg string by spaces
		if check_arguments_number(arg, 3, 3) == -1:										#Check number of arguments
			return																		#Return if not correct

		if arg[0] == 'SPOTIFY':															#if first argument is 'SPOTIFY'
			if arg[1] in list(self.spotify.keys()):										#if second argument is in spotify keys
				self.spotify[arg[1]] = arg[2]											#set spotify attribute
				print('Spotify', arg[1].capitalize().replace('_', ' '), '=', "'"+self.spotify[arg[1]]+"'", end = '\n\n')
			else:
				print('Invalid argument:', arg[1], end = '\n\n')						#else log error and return

		elif arg[0] == 'LYRICS_GENIUS':													#else if first argument is 'LYRICS_GENIUS'
			if arg[1] == 'TOKEN':														#if seconf argument is 'Token'
				self.lyrics_genius['TOKEN'] = arg[2]									#set lyrics_genius attribute
				print('Lyrics Genius Token =', "'"+self.lyrics_genius['TOKEN']+"'", end = '\n\n')
			else:
				print('Invalid argument:', arg[1], end = '\n\n')						#else log error and return

		else:
			print('Invalid argument:', arg[0], end = '\n\n')							#if first argumernt is invalid, log error and return


	def do_INIT_SESSION(self, arg):
		'''
Use: INIT_SESSION <APP> <FILE> (optional)

Dedicated to initiate an application session. To do such, you must have all
variables setted to a valid string value. You can do that using the SET command
or passing a file containing your personal data as a optional argument.

For a Spotify application, the file must contain data in
this order:
	
	username
	client_id
	client_secret
	redirect_uri

For a Lyrics Genius application, the file should contain
only your token.

Parameters:

	APP:
		SPOTIFY
		LYRICS_GENIUS
	FILE:
		A .txt file path
		'''
		arg = arg.strip().split()														#separate arg string by spaces
		if check_arguments_number(arg, 1, 2) == -1:										#check number of arguments
			return																		#return if not correct

		if arg[0] == 'SPOTIFY':															#if first argument is 'SPOTIFY'

			if len(arg) == 2:															#if provided two arguments:
				result = txt_to_list(arg[1], 4)											#get file data
				if result == -1:
					return 																#if failed, log error and return
				self.spotify = dict(zip(self.spotify.keys(), result))					#else, set spotify attribute

			for i in self.spotify.items():												#check if there are empty attributes
				if i[1] == '':
					print('Spotify', i[0], 'not specified', end = '\n\n')
					return 																#in the case, log error and return

			try:																		#try to get spotify token
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
				except:																	#if failed, log error and return
					print("Couldn't initiate Spotify application. Please, try again", end = '\n\n')

			self.spotify_api = spotipy.Spotify(auth = token)							#define spotify API object
			print('Running Spotify session', end = '\n\n')

		elif arg[0] == 'LYRICS_GENIUS':													#if first argument is 'LYRICS_GENIUS'

			if len(arg) == 2:															#if provided two arguments:
				result = txt_to_list(arg[1], 1)											#get file data
				if result == -1:
					return 																#if failed, log error and return
				self.lyrics_genius = dict(zip(self.lyrics_genius.keys(), result))		#else, set lyrics genius attributes

			for i in self.lyrics_genius.items():										#check if there are empty attributes
				if i[1] == '':
					print('Lyrics Genius', i[0], 'not specified', end = '\n\n')
					return 																#in the case, log error and return

			self.lyrics_genius_api = lyricsgenius.Genius(self.lyrics_genius['TOKEN'])	#define lyrics Genius API object
			print('Running Lyrics Genius session', end = '\n\n')

		else:
			print('Invalid argument:', arg[0], end = '\n\n')							#if first argumernt is invalid, log error and return

	def do_CLOSE_SESSION(self, arg):
		'''
Use: CLOSE_SESSION <APP>

Dedicated to stop a running application.

Parameters:

	APP:
		SPOTIFY
		LYRICS_GENIUS
		'''
		arg = arg.strip().split()														#separate arg string by spaces
		if check_arguments_number(arg, 1, 1) == -1:										#check number of arguments
			return																		#return if not correct

		if arg[0] == 'SPOTIFY':															#if first argument is 'SPOTIFY'
			if self.spotify_api == None:												#if spotify API object not defined
				print('No Spotify session currently running', end = '\n\n')				#log error and return
			else:
				self.spotify_api = None													#else set spotify API object to none
				print('Stopped Spotify session', end = '\n\n')

		elif arg[0] == 'LYRICS_GENIUS':													#if first argument is 'LYRICS_GENIUS'
			if self.lyrics_genius_api == None:											#if lyrics genius API object is none
				print('No Lyrics Genius session currently running', end = '\n\n')		#log error and return
			else:
				self.lyrics_genius_api = None 											#else set lyrics genius API object to none
				print('Stopped Lyrics Genius session', end = '\n\n')

		else:
			print('Invalid argument:', arg[0], end = '\n\n')							#if first argumernt is invalid, log error and return

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
		arg = arg.strip().split()														#separate arg string by spaces
		if check_arguments_number(arg, 1, 2) == -1:										#check number of arguments
			return																		#return if not correct

		if arg[0] in list(self.spotify.keys()):											#if second argument is in spotify keys
			print('Spotify', arg[0].capitalize().replace('_', ' '), '=', "'"+self.spotify[arg[0]]+"'", end = '\n\n')	#shows attribute
		else:
			print('Invalid argument:', arg[1], end = '\n\n')							#if first argumernt is invalid, log error and return

	def do_LYRICS_GENIUS(self, arg):
		'''
Use: LYRICS_GENIUS <VAR>

Shows Lyrics Genius app variable.

Parameters:
	
	VAR:
		TOKEN
		'''
		arg = arg.strip().split()														#separate arg string by spaces
		if check_arguments_number(arg, 1, 2) == -1:										#check number of arguments
			return																		#return if not correct

		if arg[0] in list(self.lyrics_genius.keys()):									#if second argument is in lyrics genius keys
			print('Lyrics Genius', arg[0].capitalize().replace('_', ' '), '=', "'"+self.lyrics_genius[arg[0]]+"'", end = '\n\n')	#shows attribute
		else:
			print('Invalid argument:', arg[1], end = '\n\n')							#if first argumernt is invalid, log error and return