from mongoengine import Document
from mongoengine import *

class Person(Document):
	name=StringField(max_length=50)
	email=StringField(max_length=20)
	password=StringField(max_length=10)
	mobile=StringField(max_length=10)
	address=StringField(max_length=20)