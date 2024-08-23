from os import path, makedirs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user



db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gdfwdfeygfe vgduqdfehtdfe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'}

    db.init_app(app)

   
    
    
    migrate.init_app(app, db) #bhjkhgh

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, UserProfile

    with app.app_context():
     create_database(app)
  
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))
    
       # Add this context processor
    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
     db.create_all()
    print('Created Database!')

  

    upload_folder = app.config['UPLOAD_FOLDER']
    if not path.exists(upload_folder):
        makedirs(upload_folder)
        print(f'Created upload folder at {upload_folder}')


    return app
