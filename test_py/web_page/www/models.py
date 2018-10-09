#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import time, uuid
from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
	return '%015d%s000' % (int(time.time()*1000), uuid.uuid4().hex)

class User(Model):
	__table__ = 'users'

	id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
	email = StringField(ddl='varchar(50)')
	name = StringField(ddl='varchar(50)')
	passwd = StringField(ddl='varchar(50)')
	admin = BooleanField()
	image = StringField(ddl='varchar(500)')
	created_at = FloatField(default=time.time)

class User1(Model)
	__table__ = 'users'

	id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
	username = StringField(ddl='varchar(20)')
	password = StringField(ddl='varchar(50)')
	role_number = IntegerField(ddl='int(10)')
	unit_identification = StringField(ddl='varchar(50)')
	department_identification = StringField(ddl='varchar(50)')
	employee_identification = StringField(ddl='varchar(50)')

