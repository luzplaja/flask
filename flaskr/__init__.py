import os
from flask import Flask

# application factory function
def create_app(test_config=None):
    
    # CREATE AND CONFIGURE THE APP
    app = Flask(__name__, instance_relative_config=True)    # creates the instance
    # __name__ ---> the name of the current Python module.
    # Tells the app where it’s located to set up some paths.
    
    # instance_relative_config=True ---> tells the app that configuration files are relative to the instance folder.
    # The instance folder can hold local data that shouldn’t be committed to git.
    
    app.config.from_mapping(    # default config
        SECRET_KEY = 'dev',
        # used to keep data safe. It’s set to 'dev' to provide a convenient value during development,
        # but it should be overridden with a random value when deploying.
        
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
        # path where the SQLite database file will be saved.
        # It’s under app.instance_path, which is the path that Flask has chosen for the instance folder.
    )
    
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        # app.config.from_pyfile()--->overrides the default configuration with values taken from the config.py file
        # in the instance folder if it exists. For example, when deploying, this can be used to set a real SECRET_KEY.
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        # test_config--->can also be passed to the factory, and will be used instead of the instance configuration.
        # This is so the tests you’ll write later in the tutorial can be configured independently of any development
        # values you have configured.
    
    # ensure the instance folder exits
    try: 
        os.makedirs(app.instance_path)
        # os.makedirs() ensures that app.instance_path exists.
        # Flask doesn’t create the instance folder automatically, but it needs to be created because your project
        # will create the SQLite database file there.
    except OSError:
        pass
    
    
    #######################################################################################################################
    
    
    # A SIMPLE PAGE
    
    @app.route('/hello')
    def hello():
        return 'Hello, World! :)'
    # @app.route() creates a simple route so you can see the application working before getting into the rest of
    # the tutorial. It creates a connection between the URL /hello and a function that returns a response,
    # the string 'Hello, World!' in this case.
    from . import db
    db.init_app(app)
    # Import and register the blueprint from the factory using
    # app.register_blueprint(). Place the new code at the end of the factory
    # function before returning the app.
    from . import auth
    app.register_blueprint(auth.bp)

    return app