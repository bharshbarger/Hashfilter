#!/usr/bin/env python3

import sys, os, hashlib, binascii, argparse, signal
import setupDB
from dbcommands import Database

class FilterHash():

    def __init__(self):

        self.original_potfile_dict = {}
        self.database = 'potfile.db'
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

    def ntlm_filter(self):
        original_potfile = open('potfile', "r")
        ntlm_hash_dict = {}
        hash_name = 'ntlm'
        hashcat_mode = 1000
        ntlm_potfile = open('./new_pots/ntlm.potfile', 'w+')
        print('[+] Reading potfile lines')

        #read the original potfile and get line numbers
        for i, line in enumerate(original_potfile):

            #split on first colon, maxsplit of 1 (in case colons exist in the password!)
            split_pot_entry = line.split(":", 1)

            #first split is the hash in the potfile
            hash_to_verify = str(split_pot_entry[0].rstrip("\r\n"))

            #some pots have junk and no second field, need to check
            #second split is the plaintext in the potfile
            try:
                plain_text = str(split_pot_entry[1].rstrip("\r\n"))
            except IndexError as e:
                print('weirdness on line %s' % i)

            #first quick check is length of NTLM
            if len(hash_to_verify) == 32:
                #print ('ntlm length found at %s' % i)
                #compute new ntlm based on plain from pot line
                computed_hash = hashlib.new('md4', plain_text.encode('utf-16le')).digest()
                decoded_hash = binascii.hexlify(computed_hash).decode()
                #compare entry with computed
                if decoded_hash == hash_to_verify:
                    #print ('ntlm found! suspected:%s computed: %s plain: %s ' % (hash_to_verify,decoded_hash,plain_text))
                    ntlm_potfile.writelines('%s:%s\n' % (decoded_hash, plain_text))
                    #add to new dictionary for eventual database commit
                    ntlm_hash_dict[decoded_hash] = hash_name, plain_text, hashcat_mode
            #tell user every millionth line read
            if (i % 1000000) == 0:
                print('Read %s lines' % i)
        #send to database with hash_name, hashValue, plainText, hashcatMode
        print('Adding NTLM hashes to database')
        dbOps = Database(ntlm_hash_dict)
        dbOps.add_hash()
        print('Added NTLM hashes to database')

    def sha1(self):

        hash_name = 'sha1'

        print('[+] Searching potfile for hashes with a SHA1 length')
    
    
def main():
    '''#https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', help = 'run All modes', action = 'store_true')
    parser.add_argument('-m', '--mode', help = 'specify a mode', action = 'store_true')
    parser.add_argument('-v', '--verbose', help = 'Verbose', action = 'store_true') 
    
    args = parser.parse_args()'''

    run = FilterHash()
    run.ntlm_filter()


if __name__ == '__main__':

    main()
