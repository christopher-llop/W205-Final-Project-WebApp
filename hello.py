import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello Richard, Eric and Joan!! I am a basic python WebApp.'

if __name__ == '__main__':
    app.run()