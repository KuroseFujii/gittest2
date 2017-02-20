#!/usr/bin/env python
# coding: utf-8


import RPi.GPIO as GPIO
import time
import subprocess
from time import sleep

maketext = "echo a >test.text"
confirm = "find test2.jpg"
delete = "rm test2.jpg"
dropbox = "sudo dropbox_uploader.sh upload /home/pi/test2.jpg test2.jpg"
camera = "fswebcam -F 100 /home/pi/test2.jpg"

#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
#(0, sclk, mosi, miso, ce0)sclk = 11,miso = 9,mosi = 10,ce0 = 8
def read(adcnum, sclk, mosi, miso, ce0): #cdsによって光を検出する関数を定義
      
    if adcnum > 7 or adcnum < 0:
        return -1 
    GPIO.output(ce0, GPIO.HIGH)
    GPIO.output(sclk, GPIO.LOW)
    GPIO.output(ce0, GPIO.LOW)
  
    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3
  
    for i in range(4):
        if commandout & 0x80:
            GPIO.output(mosi, GPIO.HIGH)
        else:
            GPIO.output(mosi, GPIO.LOW)
        commandout <<= 1
  
        GPIO.output(sclk, GPIO.HIGH)
        GPIO.output(sclk, GPIO.LOW)
    adcout = 0
  
    for i in range(11):
        GPIO.output(sclk, GPIO.HIGH)
        GPIO.output(sclk, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(miso) == GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(ce0, GPIO.HIGH)
    return adcout
          
GPIO.setmode(GPIO.BCM)
sclk = 11
miso = 9
mosi = 10
ce0 = 8
  
GPIO.setup(sclk, GPIO.OUT)
GPIO.setup(miso, GPIO.IN)
GPIO.setup(mosi, GPIO.OUT)
GPIO.setup(ce0, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)


try:
    while True:
        data = read(0, sclk, mosi, miso, ce0)
        print(data)
        if data < 600:
            GPIO.output(14, GPIO.HIGH)
            #time.sleep(5)
            #GPIO.output(25, GPIO.LOW)
            #time.sleep(1)
            #GPIO.output(25, GPIO.HIGH)
            sleep(0.2)
        else:
            GPIO.output(14, GPIO.LOW)
            sleep(0.2)
except KeyboardInterrupt:
    pass

GPIO.cleanup() 
