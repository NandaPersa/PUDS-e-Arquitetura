from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(app)


engine = create_engine('mysql://root:123@localhost/db', echo=False)

Session = sessionmaker(bind=engine)

base = Session()

from app.models import tables, forms
from app.controllers import principal
