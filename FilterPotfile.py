#!/usr/bin/env python
try:
	#builtin imports
	import sys, os, hashlib, binascii, argparse

	#local imports
	#import setupDB
	#from dbcommands import Database
except ImportError as e:
	raise ImportError('Error importing %s' % e)

class FilterHash():


	def __init__(self):

		self.origPotFileOpen = open('potfile', "r")
		self.newPotFileOpen=open('./new_pots/ntlm.potfile','w')
		self.hashDict={}
		self.filterHashDict={}
		self.database='potfile.db'
		


		if not os.path.exists('potfile'):
			print('\n[!] Potfile missing, please symlink "potfile" to this folder')
			sys.exit(0)

		if not os.path.exists('./new_pots'):
			print('\n[!] "./new_pots missing, creating..."')
			try:
				os.makedirs('./new_pots')	
			except Exception as e:
				print(e)
				sys.exit(0)


		if not os.path.exists(self.database):
			print('\n[!] Database missing, creating %s \n' % self.database)
			setupDB.main()


	def ntlm(self):

		hashType = 'ntlm'
		hashMode = 1000
		

		print '[+] Searching potfile for hashes with an NTLM length, then takes the plaintext and re-generates an NTLM to validate'

		#read the original potfile
		for i, line in enumerate(self.origPotFileOpen):

			#split on first colon, maxsplit of 1 (in case colons exist in the password)
			splitLine = line.split(":", 1)
			
			#take the split parts, 0 and 1 that are hash and plain, respectively
			#place into a dict and strip the \r\n off of them
			self.hashDict[str(splitLine[0].rstrip("\r\n"))]=str(splitLine[1].rstrip("\r\n"))

			#iterate the dictionary object
			for h, p in self.hashDict.items():

				#ntlm are 32 chars long, compare hashlen
				if len(h) == 32:
					
					#compute new ntlm based on plain in pot
					computedHash = hashlib.new('md4', p.encode('utf-16le')).digest()
					
					#optionally, print
					#print ('computed %s' % str(binascii.hexlify(computedHash))),
					#print (p)

					#compare entry with computed
					if binascii.hexlify(computedHash) == h:
						#print ('ntlm found! %s ' % h)
						self.newPotFileOpen.writelines('%s:%s\n'%(h,p))

						#add to new dictionary for eventual database commit
						self.filterHashDict[h]=hashType,p,hashMode


			'''if self.args.useDatabase is True:
			#send to database with hashType, hashValue, plainText, hashcatMode
				dbOps = Database(self.filterHashDict)
				dbOps.add_hash()'''	


	def sha1(self):

		hashType = 'sha1'

		print '[+] Searching potfile for hashes with a SHA1 length'
	
	
def main():




	'''#https://docs.python.org/3/library/argparse.html
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--all', help = 'run All modes', action = 'store_true')
	parser.add_argument('-m', '--mode', help = 'specify a mode', action = 'store_true')
	parser.add_argument('-v', '--verbose', help = 'Verbose', action = 'store_true')	
	
	args = parser.parse_args()'''
	
	run=FilterHash()
	run.ntlm()


if __name__ == '__main__':

	main()
