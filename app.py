from flask import Flask, request, session, abort
import markupsafe
import config

def check_csrf():
    token_form = request.form.get("csrf_token", "")
    token_session = session.get("csrf_token", "")
    if not token_session or token_form != token_session:
        abort(403)

app = Flask(__name__)
app.secret_key = config.secret_key


@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

from user import init_user
from reviews import init_reviews

init_user(app)
init_reviews(app)