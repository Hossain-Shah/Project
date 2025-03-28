import datetime
import threading
import playsound
print(datetime.datetime.today().strftime("%H"))
print(datetime.datetime.today().strftime("%M"))
time = int(input("Enter a duration: "))


def hello():
    playsound.playsound('Twin-bell-alarm-clock-sound.mp3')


if __name__ == '__main__':
    t = threading.Timer(time, hello)
    t.start()
