import argparse

from app import App

parser = parser = argparse.ArgumentParser(description = "App for information gathering from \
														 Spotify and Lyrics Genius API's")		#defines argument parser with its description

parser.add_argument('-f', '--file', type = str,
					required = True, help = 'File with credentials')							#defines composer argument


args = parser.parse_args()																		#gets parsed arguments

init_message = '''
\t***********************************
\t|Welcome to MusicInfo Environment!|
\t***********************************
'''

app = App(file=args.file)
app.prompt = '> '
app.cmdloop(init_message)
