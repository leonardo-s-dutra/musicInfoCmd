from app import App

init_message = '''
\t***********************************
\t|Welcome to MusicInfo Environment!|
\t***********************************
'''

app = App()
app.prompt = '> '
app.cmdloop(init_message)
