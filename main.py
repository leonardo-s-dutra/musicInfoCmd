from app import App

init_message = '''
\t***************************
\t|Welcome to py music info!|
\t***************************
'''

app = App()
app.prompt = '> '
app.cmdloop(init_message)
