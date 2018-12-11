import os


def txt_to_list(file, number_of_lines):

	if not os.path.exists(file):
		print('Could not find file', "'"+file+"'", end = '\n\n')
		return -1

	try:
		with open(file) as f:

			lines = [line.replace('\n', '') for line in f.readlines()]

			if len(lines) < number_of_lines:
				print('Missing values in file', "'"+file+"'", end = '\n\n')
				return -1

			elif len(lines) > number_of_lines:
				print('Too many values in file', "'"+file+"'", end = '\n\n')
				return -1

			return lines

	except:
		print('Could not open file', "'"+file+"'", end = '\n\n')
		return -1


def check_arguments_number(arg, min, max):

	if len(arg) < min:
		print('Missing arguments!', end = '\n\n')
		return -1

	elif len(arg) > max:
		print('Too many arguments!', end = '\n\n')
		return -1

	else:
		return 0


def get_artist_id(artist_name, spotipyObject):

	search = spotipyObject.search(q = 'artist:' + artist_name, type = 'artist')['artists']['items']
	
	if len(search) > 0:
		return search[0]
	else:
		return -1


def get_album_id(album_name, spotipyObject):

	search = spotipyObject.search(q = 'album:' + album_name, type = 'album')['albums']['items']
	
	if len(search) > 0:
		return search[0]
	else:
		return None


def get_albums(artist, spotipyObject):

	search = spotipyObject.artist_albums(artist['id'], album_type = 'album')

	albums = []
	albums.extend(search['items'])
	while search['next']:
		search = spotipyObject.next(search)
		albums.extend(search['items'])

	added = set()
	for album in albums:
		name = re.sub("[(].*?[)]", '', album['name'].split(':')[0].split(' - ')[0]).strip()
		added.add(name)

	return added


def get_artist_top_tracks(artist, country = None):

	search = spotipyObject.artist_top_tracks(artist['id'])['tracks']

	added = set()
	for track in search:
		name = re.sub("[(].*?[)]", '', track['name'].split(':')[0].split(' - ')[0]).strip()
		added.add(name)

	return added


def get_album_tracklist(album):

	search = spotipyObject.album(album['id'])['tracks']['items']

	added = set([i['name'] for i in search])

	return added

def get_song_lyrics(name, artist):

	song = geniusObject.search_song(name, artist)

	if song == None:
		print('\nNo lyrics found for ' + name + '\n')
		return -1

	if song.lyrics.lower().find('instrumental') != -1:
		print('\nNo lyrics found for ' + song.title + '\n')
		return -1

	return song.lyrics