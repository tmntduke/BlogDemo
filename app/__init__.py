from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object('config')

# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '20140316'
# app.config['MYSQL_DATABASE_DB'] = 'tmnt'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:20140316@localhost:3306/tmnt')
DBSession = sessionmaker(bind=engine)
from app import views
