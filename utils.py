import os
import re


def txt_to_list(file):

	if not os.path.exists(file):
		print('Could not find file', "'"+file+"'", end = '\n\n')
		return -1

	try:
		with open(file) as f:

			lines = [line.replace('\n', '') for line in f.readlines()]

			if len(lines) < 5:
				print('Missing values in file', "'"+file+"'", end = '\n\n')
				return False

			elif len(lines) > 5:
				print('Too many values in file', "'"+file+"'", end = '\n\n')
				return False

			return lines

	except:
		print('Could not open file', "'"+file+"'", end = '\n\n')
		return -1


def check_arguments_number(arg, min = 0, max = float('inf')):

	if len(arg) < min:
		print('Missing arguments!', end = '\n\n')
		return -1

	elif len(arg) > max:
		print('Too many arguments!', end = '\n\n')
		return -1


def print_table(items):

	max_len = max(len(item) for item in items)

	print('\t' + max_len * '*' + '**')
	for item in items:
		print('\t|' + item + (max_len - len(item)) * ' ' + '|')
	print('\t' + max_len * '*' + '**', end = '\n\n')


def get_artist_id(artist_name, spotipyObject):

	try:
		search = spotipyObject.search(q = 'artist:' + artist_name, type = 'artist')['artists']['items'][0]

	except IndexError:
		return -1

	return search['id']


def get_album_id(album_name, spotipyObject):

	try:
		search = spotipyObject.search(q = 'album:' + album_name, type = 'album')['albums']['items'][0]
	
	except IndexError:
		return -1

	except TypeError:
		return -1

	return search['id'], search['artists'][0]['name']


def get_artist_albums(artist, spotipyObject):

	artist_id = get_artist_id(artist, spotipyObject)

	try:
		search = spotipyObject.artist_albums(artist_id, album_type = 'album')

		albums = []
		albums.extend(search['items'])
		while search['next']:
			search = spotipyObject.next(search)
			albums.extend(search['items'])

		return set([re.sub("[(].*?[)]", '', album['name'].split(':')[0].split('-')[0]).strip() for album in albums])

	except AttributeError:
		return -1


def get_album_tracklist(album, spotipyObject):

	try:
		album_id, artist = get_album_id(album, spotipyObject)

	except TypeError:
		return -1, None

	try:
		search = spotipyObject.album(album_id)['tracks']['items']

		return set([i['name'] for i in search]), artist

	except AttributeError:
		return -1, None


def get_artist_top_tracks(artist, spotipyObject, country = None):

	artist_id = get_artist_id(artist, spotipyObject)

	try:
		search = spotipyObject.artist_top_tracks(artist_id)['tracks']

		return set([re.sub("[(].*?[)]", '', track['name'].split(':')[0].split('-')[0]).strip() for track in search])

	except AttributeError:
		return -1


def get_song_lyrics(name, artist, lyricsGeniusObject):

	song = lyricsGeniusObject.search_song(name, artist)

	if song == None:
		print('\nNo lyrics found for ' + name.capitalize(), end = '\n\n')
		return -1

	if song.lyrics.lower().find('[Instrumental]') != -1:
		print('\nNo lyrics found for ' + song.title, end = '\n\n')
		return -1

	return song.lyrics, song.artist