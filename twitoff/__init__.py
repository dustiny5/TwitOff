"""
Entry point for TwitOff.
"""

from .app import create_app

APP = create_app()

# 1. Go to TwitOff directiory
#   - In gitbash, 
#       - type - pipenv install Flask
#       - type - pipenv shell - activates virtual environment
#       - type - FLASK_APP=twitoff flask run
#       - Or type - FLASK_APP=twitoff:APP flask run
#       - type - pipenv install flask-sqlalchemy
#           - to run sql
#       - type - FLASK_APP=twitoff:APP flask shell
#           - To run flask stuff