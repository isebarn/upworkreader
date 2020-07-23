import os
import json

from datetime import datetime

from sqlalchemy import ForeignKey, desc, create_engine, func, Column, BigInteger, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if os.environ.get('DATABASE') is not None:
  connectionString = os.environ.get('DATABASE')

engine = create_engine(connectionString, echo=False)

Base = declarative_base()

class Keywords(Base):
  __tablename__ = 'keywords'
  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', Text)

class Ad(Base):
  __tablename__ = 'ads'

  Id = Column('id', Text, primary_key=True)
  Title = Column('title', Text)
  Url = Column('url', Text)
  Payment = Column('payment', Text)
  Time = Column('time', DateTime)

  def __init__(self, data):
    self.Id = data['id']
    self.Title = data['title']
    self.Url = data['url']
    self.Payment = data['payment']
    self.Time = datetime.now()

  def Readable(self):
    result = {}

    result['id'] = self.Id
    result['title'] = self.Title
    result['url'] = self.Url
    result['payment'] = self.Payment
    result['time'] = self.Time

    return result

class Operations:

  def GetAllKeywords():
    return [x.Value for x in session.query(Keywords).all()]

  def GetAllIds():
    return [x[0] for x in session.query(Ad.Id).all()]

  def GetAll():
    return [x for x in session.query(Ad).all()]

  def SaveAd(data):
    ad = Ad(data)

    exists = session.query(Ad.Id
      ).filter_by(Id=ad.Id
      ).scalar() != None

    if not exists:
      session.add(ad)
      session.commit()


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


if __name__ == "__main__":
  print(os.environ.get('DATABASE'))
  print(Operations.GetAll())
