from flask import Flask
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = 'static/upload/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

bootstrap = Bootstrap(app)