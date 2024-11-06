#!/usr/bin/env python3
"""ALX Backend project with Flask"""

from flask import (Flask, render_template, request, g)
from typing import (Dict, Union)
from flask_babel import Babel
from datetime import timezone
from pytz import timezone
import pytz.exceptions


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Babel config"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


def get_user() -> Union[Dict, None]:
    """
    Returns a dictionary representing the user or None
    if the ID value is not found or if the 'login_as' parameter
    is missing from the URL.
    """
    user_id = request.args.get('login_as', None)
    if user_id is not None and int(user_id) in users.keys():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """If a user exists, log them in."""
    login_user = get_user()
    g.user = login_user


@babel.timezoneselector
def get_timezone():
    """Try and get user timezone, and if not succeeded, use the default"""
    user_timezone = request.args.get('timezone', None)
    if user_timezone:
        try:
            return timezone(user_timezone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            user_timezone = g.user.get('timezone')
            return timezone(user_timezone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    babel_fallback_timezone = app.config['BABEL_DEFAULT_TIMEZONE']
    return babel_fallback_timezone


@babel.localeselector
def get_locale():
    """Checks if locale lang is supported and match if it does."""
    user_local = request.args.get('locale')
    if user_local in app.config['LANGUAGES']:
        return user_local
    if g.user:
        user_local = g.user.get('locale')
        if user_local and user_local in app.config['LANGUAGES']:
            return user_local
    user_local = request.headers.get('locale', None)
    if user_local in app.config['LANGUAGES']:
        return user_local
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Configs the route for the home page"""
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
