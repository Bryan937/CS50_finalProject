from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import insert, delete, update, create_engine
from sqlalchemy.sql import select


# Set application
app = Flask(__name__)

# Configure application
app.config['SECRET_KEY'] = '1745b62e3de350cbb2f96976bdc649e1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LGA.db'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg', '.pdf']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from website import routes