#V 0.1.0
#By Andre Metelo (metelo@gmail.com)
# Initial release date:	2022/02/23
# Licensed unde GPL 3.0
"""
Requirements:
	-> mysql.connector in python
	-> unidecode if we keep the ASCII only versions of the queries
	-> uuid
	-> This should work for both Python 2 and 3, as the 1st line
	   sets the enconding the UTF-8

Some todos:
	 -> Better error handling
	 -> Not sure if it is a good idea or not fo force the data through unidecode to have 
	    ASCII only characters, as MYSQl already defaults to utf-8. But it can be used
	    in some cases (like Gov data that still use ASCII/EDBC charsets)
	 -> Better info in the list all connections functions. Maybe add DB and server info
"""

#Class to manage MYSQL connections within RobotFramework.

import unidecode
import mysql.connector
import uuid

#Should I write an ASCII version of the execute/executemany/fetch methods? or simply drop UTF to ASCII encode completely?
class mysqlwrapper(object):

	#initiate internal Dicts with current active connections and cursors
	#this is to allow for multiple DB Connections
	def __init__(self):
		self.connections_internal = {}
		self.cursors_internal = {}

	#This is a function to remove all unicode and convert to ASCII if we desire to use ASCII DB
	#Specially useful for languages like Spanish and Portuguese
	def to_ascii(self, string):
		string = unidecode.unidecode(string)
		return string

	#This will generate a unique string for each connection and cursor 
	#For internal use.
	def create_uuid(self):
		myuuid = uuid.uuid4()
		return str(myuuid)

	#This will create a cocnnection and cursor for the DB. It
	#It returns a UUID if all works, and -1 in case of connection error
	def connect_to_db(self, host, user, password, database):
		mydb = mysql.connector.connect(
			host=dbserver,
			user=dbuser,
			password=dbpwd,
			database=MEIdatabase)
		mycursor = mydb.cursor()
		if mydb.is_connected():
			myuuid = self.create_uuid()
			self.connections_internal['myuuid'] = mydb
			self.cursors_internal['myuuid'] = mycursor
			return myuuid
		else:
			return	-1	#Connection failed.

	#This will close the connection and cursor and remove them from the active list
	def close_db(self, myuuid):
		mycursor = self.cursors_internal['myuuid']
		mydb = self.connections_internal['myuuid']
		mycursor.close()
		mydb.close()
		del self.cursors_internal['myuuid']
		del self.connections_internal['myuuid']
		if mydb.is_connected():
			return -1
		else:
			return True

	#This will close all connections and cursor and remove them from the active list
	def close_db_all_connections(self, myuuid):
		for mycursor in self.cursors_internal:
			mycursor.close()
		for mydb in self.connections_internal:
			mydb.close()
		self.cursors_internal.clear()
		self.connections_internal.clear

	def list_open_connections(self):
		return self.connections_internal['myuuid']

	#SQl to be called using the %s syntax to protect against injection
	#data to be passed as list, and function will convert to tuple
	def execute_sql(self, myuuid, sql, data):
		mycursor = self.cursors_internal['myuuid']
		mydb = self.connections_internal['myuuid']
		if mydb.is_connected():
			tupledata = tuple(data)
			mycursor.execute(sql, tupledata)
			mydb.commit()
			#Todo -> better error handling
			return True
		else:
			return -1

	#See execute for specifics
	def executemany_sql(self, myuuid, sql, datalist):
		mycursor = self.cursors_internal['myuuid']
		mydb = self.connections_internal['myuuid']
		if mydb.is_connected():
			tupledatalist = [tuple(e) for e in (datalist)]
			mycursor.executemany(sql, tupledatalist)
			mydb.commit()
			#Todo -> better error handling
			return True
		else:
			return -1

	#Run the SQL and return all responses
	#SQL can use limit and offset to control where the data starts and how many records are returned
	def fetch_sql(self, myuuid, sql):
		mycursor = self.cursors_internal['myuuid']
		mydb = self.connections_internal['myuuid']
		if mydb.is_connected():
			mycursor.execute(sql)
			myresult = mycursor.fecthall()
			return	myresult
		else:
			return -1
