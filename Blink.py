from neo import Gpio  # import Gpio library
from time import sleep  # import sleep to wait for blinks

neo = Gpio()  # create new Neo object
pin = 2

def b_on():
        neo.pinMode(pin, neo.OUTPUT)
        neo.digitalWrite(pin, neo.HIGH)

def b_off():
        neo.pinMode(pin, neo.INPUT)
        neo.digitalWrite(pin, neo.LOW)

def blink():
        neo.pinMode(pin,neo.OUTPUT)

        for a in range(0,5):
                neo.digitalWrite(pin, neo.HIGH)  # write high value to pin
                print ("Clap!")
                sleep(1)
                neo.digitalWrite(pin, neo.LOW)  # write low value to pin
                sleep(1)


