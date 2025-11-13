from flask import Flask
import config

app = Flask(__name__)
app.secret_key = config.secret_key

from user import init_user
from reviews import init_reviews

init_user(app)
init_reviews(app)