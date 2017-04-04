#!/usr/bin/env python
try:
	#builtin imports
	import sys, os, hashlib, binascii

	#local imports
	import setupDB
	from dbcommands import Database
except ImportError as e:
	raise ImportError('Error importing %s' % e)

class FilterHash():


	def __init__(self):


		if not os.path.exists('potfile'):
			print('\n[!] Potfile missing, please symlink to this folder')
			sys.exit(0)



		self.origPotFileOpen = open('potfile', "r")
		self.newPotFileOpen=open('./new_pots/ntlm.potfile','w')
		self.hashDict={}
		self.filterHashDict={}
		self.database='potfile.db'


		if not os.path.exists(self.database):
			print('\n[!] Database missing, creating %s \n' % self.database)
			setupDB.main()
		

	def ntlm(self):

		hashType = 'ntlm'
		hashMode = 1000
		

		print '[+] Searching potfile for hashes with an NTLM length, then takes the plaintext and re-generates an NTLM to validate'

		#read the original potfile
		for i, line in enumerate(self.origPotFileOpen):

			#split on first colon
			splitLine = line.split(":")[0]
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

						#add to new dictionary for eventual database commit
						self.filterHashDict[h]=hashType,p,hashMode
		
			#send to database with hashType, hashValue, plainText, hashcatMode
			dbOps = Database(self.filterHashDict)
			dbOps.add_hash()	

	
		

	def sha1(self):

		hashType = 'sha1'

		print '[+] Searching potfile for hashes with a SHA1 length'
	
	'''#iterate the dictionary containing user and hashes
	for h, u in self.hashDict.items():
		#write username to text file
		self.newPotFileOpen.writelines(str(u)+'\n')
		#write username to credResult for the docx report
		credResult.append(str(u)+'\n')
		
	self.newPotFileOpen.writelines('********CREDENTIALS FOUND BELOW*********\n\n\n\n')
	credResult.append('********CREDENTIALS FOUND BELOW*********\n\n\n\n')
	
	#this section 'cracks' the hashes provided a pre-populated pot file
	#still in our lookup value iterate potfiles directory. you can have multiple pots, just in case
	for potFileName in os.listdir('./potfile/'):
		#open a pot file
		with open('./potfile/'+potFileName, 'r') as potFile:
			#tell user you are looking
			print '[i] Any creds you have in your potfile will appear below as user:hash:plain : '
			#then look at every line
			for potLine in potFile:
				#then for every line look at every hash and user in the dict
				for h, u in self.hashDict.items():
					#if the hash in the dict matches a line in the potfile
					#that is also the same length as the original hash (this is probably a crappy check tho...)
					if str(h) == str(potLine[0:len(h)]):
						#print the user: and the line from the potfile (hash:plain) to the user
						print str(u)+':'+str(potLine.rstrip("\r\n"))
						#need to append the output to a variable to return or write to the file
						#this is separate because not all found usernames/emails have hashes and not all hashes are cracked
						#write to text file
						self.newPotFileOpen.writelines(str(u)+':'+str(potLine[len(h):]))
						#add to credResult for docx report
						credResult.append(str(u)+':'+str(potLine[len(h):]))


	return credResult	
	print credResult'''

def main():
	
	run=FilterHash()
	run.ntlm()


if __name__ == '__main__':

	main()
