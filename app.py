from flask import Flask, request, session, abort
import config

def check_csrf():
    token_form = request.form.get("csrf_token", "")
    token_session = session.get("csrf_token", "")
    if not token_session or token_form != token_session:
        abort(403)

app = Flask(__name__)
app.secret_key = config.secret_key

from user import init_user
from reviews import init_reviews

init_user(app)
init_reviews(app)