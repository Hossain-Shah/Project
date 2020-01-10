import speech_recognition as sr
print(sr.__version__)
r = sr.Recognizer()
harvard = sr.AudioFile('harvard.wav')
with harvard as source:
    audio = r.record(source)
    type(audio)
    print(r.recognize_google(audio))

jackhammer = sr.AudioFile('jackhammer.wav')
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
    audio1 = r.record(source)
    print(r.recognize_google(audio1))