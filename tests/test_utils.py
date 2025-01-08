import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


database_url = "sqlite:///./test.db"
engine = create_engine(database_url)
session_maker = sessionmaker(bind=engine)
