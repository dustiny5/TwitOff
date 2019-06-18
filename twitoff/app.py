"""
Main application and routing/configuration logic for TwitOff
"""

from flask import Flask, render_template, request
from .models import DB, User
from decouple import config # Reads our .env file

def create_app():
    """ Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Warning goes away
    app.config['ENV'] = config('ENV') # Shows detailed error # Don't deploy
    DB.init_app(app)

    # Root route
    @app.route('/')
    def root():
        users = User.query.all()
        # Look inside template directory
        return render_template('base.html', title='Home', users=users)
    
    # Convenient reset
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])
    return app