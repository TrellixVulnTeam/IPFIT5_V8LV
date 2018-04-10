import hashlib
import sqlite3


def hashfile(inputfile):
    read_size = 1024  # You can make this bigger
    checksumsha256 = hashlib.sha256()

    try:
        with open(inputfile, 'rb') as f:
            data = f.read(read_size)
            while data:
                checksumsha256.update(data)
                data = f.read(read_size)
        checksumsha256 = checksumsha256.hexdigest()

        # shows de hashes in the terminal
        print("File Name: %s" % inputfile)
        print("SHA256: %r" % checksumsha256)
        print("")

        with open("ChecksumLog.txt", "a") as myfile:  # This writes the hashes to a file
            myfile.write("File Name: %s" % inputfile + "\n")
            myfile.write("SHA256: %r" % checksumsha256 + "\n")
            myfile.write("\n")

        conn = sqlite3.connect("Hash.db")
        c = conn.cursor()
        # Make table with 3 columns: File, MD5 and SHA256
        c.execute("CREATE TABLE IF NOT EXISTS Hash(File TEXT, SHA256 TEXT)")
        c.execute('INSERT INTO Hash VALUES(?,?)', (inputfile, checksumsha256))
        conn.commit()

    except IOError:
        print("There is no such file")


def clearfile():  # Clear the log file
    open("ChecksumLog.txt", 'w').close()
    print("")
    print("Log file cleared")
