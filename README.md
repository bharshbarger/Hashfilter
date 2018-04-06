# Hashfilter
Read a hashcat potfile and parse different types into a sqlite database and hash-specific potfiles based on the mode number hashcat uses, like -m 1000 for ntlm. Takes the original pot file reads the hash and plain, then rehashes the plain to make sure the entry is valid, then logs to a new sorted potfile, or optionally a sqlite database.


    usage: FilterPotfile.py [-h] [-m [MODE [MODE ...]]] [-d] [-v]

    optional arguments:
    -h, --help            show this help message and exit
    
    -m [MODE [MODE ...]], --mode [MODE [MODE ...]]
                         specify a mode
                         
    -d, --database        log sorted hashes to a database
    
    -v, --verbose         Verbose
    

