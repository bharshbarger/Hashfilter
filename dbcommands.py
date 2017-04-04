#!/usr/bin/env python


import sqlite3


class Database:

	def __init__(self,filterHashDict):

		self.filterHashDict = filterHashDict
		self.potfileDB = 'potfile.db'

	def connect(self):

		try:
			dbconn = sqlite3.connect(self.potfileDB)
		except sqlite3.Error as e:
			print("[-] Database Error: %s" % e.args[0])
		return dbconn

	def add_hash(self):

		dbconn=self.connect()
		cur = dbconn.cursor()

		#for hashval, plaintext, hashcatmode, and hashtype
		for h,p,m,t in self.filterHashDict.items():

	

			#insert rows
			#print('ID___ Mode_ Value___________________________________ Type____  Plain_______________________')


			#check to see if the hash exists, and if it does print it, and if it doesnt add it
			try:
				'''#look for existing hash from supplied arg
				cur.execute("SELECT * FROM hashvalue WHERE (type = '%s') " % (t))
				results = cur.fetchall()
				cur.close()

				#if there is a result
				if results is not None:
					#print it
					for row in results:
						print ('%-5s %-5s %-8s %s' % (row[0], row[1], row[2], row[3]))
				#if there isn't a result
				else:
					#add customer
					try:'''
				cur.execute("INSERT INTO hashtypes (hashname, hashcatmode) VALUES ('%s, %s') " % (t,m))
				dbconn.commit()
				cur.execute("INSERT INTO hashvalue (value, type) VALUES ('%s, %s') WHERE type=%s " % (h,t,t))
				dbconn.commit()
				cur.execute("INSERT INTO plain (plaintext, type) VALUES ('%s, %s') WHERE type=%s " % (h,t,t))
				dbconn.commit()

				'''#and display it
				cur.execute("SELECT * FROM client WHERE (name = '%s') " % (c))
				results = cur.fetchall()'''
				cur.close()
			except sqlite3.Error as e:
				print("[-] Database Error: %s" % e.args[0])



	print('\n')


def main():

	dbOps=Database()
	#dbOps.connect()



if __name__ == '__main__':
	main()