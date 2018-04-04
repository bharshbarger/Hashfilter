#!/usr/bin/env python3

try:
	import sqlite3
except ImportError as e:
	raise ImportError('Error importing %s' % e)

class PotfileDatabase():
	def __init__(self):
		
		#vars
		self.potfileDB = 'potfile.db'

	def createdatabase(self):

		# Database Connection
		print('[i] Creating Database')
		try:
			connection = sqlite3.connect(self.potfileDB)
			c = connection.cursor()

			#Create table
			c.execute('''CREATE TABLE client(
				ID INTEGER PRIMARY KEY,
				name text, 
				Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
				UNIQUE(name))''')
			
			c.execute('''CREATE TABLE plain(
				ID INTEGER PRIMARY KEY,
				plaintext text,
				hash_val text,
				type text,
				client_id integer, 
				FOREIGN KEY(client_id) REFERENCES client(ID),
				FOREIGN KEY(hash_val) REFERENCES hashvalue(value))''')
			
			c.execute('''CREATE TABLE hashvalue(
				ID INTEGER PRIMARY KEY, 
				value text,
				plain_text text, 
				type text,
				client_id integer,
				FOREIGN KEY(type) REFERENCES hashtypes(hashname),
				FOREIGN KEY(client_id) REFERENCES client(ID),
				FOREIGN KEY(plain_text) REFERENCES plain(plaintext)) ''')
			
			c.execute('''CREATE TABLE hashtypes(
				ID INTEGER PRIMARY KEY, 
				hashname text, 
				hashcatmode integer,
				UNIQUE(hashname),
				UNIQUE(hashcatmode))''')

			print('[i] Populating NTLM type')
			c.execute("INSERT INTO hashtypes (hashname, hashcatmode) VALUES ('ntlm','1000') ")

			# Commit and close connection to database
			connection.commit()
			connection.close()

		except sqlite3.Error as e:
			print(" [-] Database Error: %s" % e.args[0])

def main():
	createDb = PotfileDatabase()
	createDb.createdatabase()


if __name__ == '__main__':
	main()
