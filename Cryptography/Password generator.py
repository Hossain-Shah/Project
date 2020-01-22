import random
alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
length = input('Password length:')
length = int(length)
password = ''
for c in range(length):
    password += random.choice(alphabet)
print(password)
