"""
Main application and routing/configuration logic for TwitOff
"""

from decouple import config # Reads our .env file
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_user

def create_app():
    """ Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    # the config(...) is from the .env # Save to the database
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Warning goes away
    # app.config['ENV'] = config('ENV') # Not necessary added to .env
    DB.init_app(app)

    # Root route
    @app.route('/')
    def root():
        users = User.query.all()
        # Look inside template directory
        return render_template('base.html', title='Home', users=users)
    
    # Convenient reset - Not for deployment
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])
    # Apply to user.html
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # Request values is coming from the user enpoint ['POST']
        # Get name exist from get request or from the post request if no name
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)
    # Apply to predict.html
    @app.route('compare', methods=['POST'])
        user1, user2 = sorted([request.values['user1'], 
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
            else:
                prediction = predict_user(user1, user2,
                                           request.values['tweet_text'])
                message = '"{}" is more likely to be said by {} than {}'.format(
                    request.values['tweet_text'], user1 if prediction else user2,
                    user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)


    
    '''
    # Class
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # Request values is coming from the user enpoint ['POST']
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} Successfully Added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error Adding {}: {}".format(name, e)
        return render_template('user.html', title=name, tweets=tweets, message=message)
    '''

    return app
