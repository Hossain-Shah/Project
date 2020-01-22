import bcrypt
from urllib.request import urlopen, hashlib
#Demonstrates the difference between two types of hashing, SHA1 and Bcrypt
password = input("Input the password to hash\n>")
print("\nSHA1:\n")
for i in range(3):
    setpass = bytes(password, 'utf-8')
    hash_object = hashlib.sha1(setpass)
    guess_pw = hash_object.hexdigest()
    print(guess_pw)
print("\nMD5:\n")
for i in range(3):
    setpass = bytes(password, 'utf-8')
    hash_object = hashlib.md5(setpass)
    guess_pw = hash_object.hexdigest()
    print(guess_pw)
print("\nBCRYPT:\n")
for i in range(3):
    
    hashed = bcrypt.hashpw(setpass, bcrypt.gensalt(10))
sha1hash = input("Please input the hash to crack.\n>")
urlopen('TheURLYouWantToOpen').read()
LIST_OF_COMMON_PASSWORDS = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt').read(), 'utf-8')
for guess in LIST_OF_COMMON_PASSWORDS.split('\n'):
    hashedGuess = hashlib.sha1(bytes(guess, 'utf-8')).hexdigest()
    if hashedGuess == sha1hash:
        print("The password is ", str(guess))
        quit()
    elif hashedGuess != sha1hash:
        print("Password guess ",str(guess)," does not match, trying next...")
print("Password not in database, we'll get them next time.")
