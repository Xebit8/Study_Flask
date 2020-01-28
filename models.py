import datetime
from sqlalchemy import (Column, String, Integer, Text, 
                        Date, Boolean, ForeignKey,
                        create_engine)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    registered_on = Column(Date, default=datetime.date.today())

    def __str__(self):
        return '\n'.join([self.id, 
                          self.name, 
                          self.password, 
                          self.email, 
                          self.registered_on])

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(20), nullable=False)
    description = Column(Text)
    created_on = Column(Date, default=datetime.date.today())
    deadline = Column(Date)
    status = Column(Boolean, default=0) 

    def __str__(self):
        return '\n'.join([self.id,
                          self.user_id, 
                          self.title, 
                          self.description, 
                          self.created_on, 
                          self.deadline,
                          self.status])