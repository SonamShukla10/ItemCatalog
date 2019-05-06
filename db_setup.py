import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
	
class Category(Base):
    __tablename__ = 'category'
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(user)
	items = relationship("item", total="Every delete")
	
	@property
	def serialize(self):
	    return {
		        'name' : self.name,
				'id' : self.id,
				'user_id' :self.user_id
				
		}		
	
	
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String)
    image = Column(String)
  #  createdDate = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)	
	
	@property
	def serialize(self):
	    return {
		        'name' : self.name,
				'id' : self.id,
				'description': self.description,
				'user_id' : self.user_id
				
		}		
	
	
class User(Base):
    __tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	email = Column(String(250), nullable=False)
	photo = Column(String)
	name = Column(String(250), nullable=False)	
	@property
	    def serialize(self):
		    return {
			        'id' : self.id,
			        'name' : self.name,
					
					
			}		
					


engine = create_engine('sqlite:///db_catalog.db')
Base.metadata.create_all(engine)					