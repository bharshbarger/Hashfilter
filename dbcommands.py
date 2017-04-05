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
		self.connect()
		dbconn=self.connect()
		cur = dbconn.cursor()

		#for hashval, plaintext, hashcatmode, and hashtype
		for h,vals in self.filterHashDict.items():
			m=str(vals[2])
			p=str(vals[1])
			t=str(vals[0])
			h=str(h)


			print h,t,m,p

			
			#try:
			cur.execute("INSERT OR IGNORE INTO hashtypes (hashname, hashcatmode) VALUES ('%s', '%s') " % (t,m))
			dbconn.commit()
			cur.execute("INSERT INTO hashvalue (value, type) VALUES ('%s', '%s') WHERE (type='%s') " % (h,t,t))
			dbconn.commit()
			cur.execute("INSERT INTO plain (plaintext, type) VALUES ('%s', '%s') WHERE (type='%s') " % (h,t,t))
			dbconn.commit()

			#and display it
			cur.execute("SELECT * FROM client WHERE (name = '%s') " % (c))
			results = cur.fetchall()
			cur.close()
			'''except sqlite3.Error as e:
				print("[-] Database Error: %s" % e.args[0])'''



	print('\n')


def main():

	dbOps=Database()
	

if __name__ == '__main__':
	main()