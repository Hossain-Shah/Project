import numpy as np
wordlist="hello how are you can you read this without punctuation do you think this is something what is the meaning of life".split()
wordlist=[word for word in wordlist if len(word) == 3]
wordlist=[word for word in wordlist if word[0].islower()]
wordlist=[word for word in wordlist if word.isalpha()]
wordlist = list(map(str.lower, wordlist))
print(len(wordlist))
wordlist=np.asarray(wordlist)
print(wordlist.dtype)
wordlist.sort()
i1=wordlist.searchsorted('wade')
i2=wordlist.searchsorted('hate')
print(wordlist[i1])
print(wordlist[i2])
print(wordlist)
