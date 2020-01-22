alphabet = 'abcdefghijklmnopqrstuvwxyz'
key = 3
newMessage = ''
message = input('Enter text:')
for character in message:
    position = alphabet.find(character)
    newPosition = (position + key) % 26
    newCharacter = alphabet[newPosition]
    newMessage += newCharacter
print('Ciphered new text:',newMessage)
