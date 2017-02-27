#!/usr/bin/env python
# coding: utf-8


import RPi.GPIO as GPIO
import time
import subprocess
from time import sleep
picnum =1   #保存する写真する名前の数字の初期値

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

def take_a_picture(): # 写真を撮影する関数を定義
    confirm = "locate test1.jpg"
    updatedb = "sudo updatedb"
    delete = "rm test1.jpg"
    dropbox = "sudo dropbox_uploader.sh upload /home/pi/test1.jpg test1.jpg"
    camera = "fswebcam -F 100 /home/pi/test1.jpg"
    confirm = confirm.replace('test1','test'+str(count)) #保存する写真する名前の数字を変更
    delete = delete.replace('test1','test'+str(count)) #保存する写真する名前の数字を変更
    dropbox = dropbox.replace('test1','test'+str(count)) #保存する写真する名前の数字を変更
    camera = camera.replace('test1','test'+str(count)) #保存する写真する名前の数字を変更
    while True:
        print('check to exist a picture_data')
        ret  =  subprocess.call(confirm,shell = True)
        if ret == 0: #cmdの結果はcatコマンドで画像があれば0を返し、なければ1を返す
            print ret == 0   #File is existed
            print('picture_data is existed.Delete!')
            subprocess.call(delete,shell = True) #file delete
            break
        else:
            #print "non file" #File is not existed
            break
    while True:
        print('Take a picture')
        subprocess.call(camera,shell = True)
        subprocess.call(updatedb,shell = True)
        print('check to exist a picture_data_2nd')
        ret  =  subprocess.call(confirm,shell = True)

        if ret == 0: #cmdの結果はcatコマンドで画像があれば0を返し、なければ1を返す
            print ret == 0   #File is existed
            print('picture_data is existed.Upload!')
        else:
            print "we can't take a picture" #File is not existed
            print('one more take a picture')
            print('Waitig for 10 sec ')
            GPIO.output(4, GPIO.HIGH)
            time.sleep(10)
            GPIO.output(4, GPIO.LOW)
            time.sleep(10)
            continue
        subprocess.call(dropbox,shell = True) # upload
        print "dropbox upload success"
        print 'count=' + str(count)
        break 
          
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
        data = read(0, sclk, mosi, miso, ce0) #ドアが開いたことを確認するデータを取得
        print('data = %s'% data)
        if data > 900: 
            while True:
                data2 = read(0, sclk, mosi, miso, ce0) #ドアが開いたことを確認するデータを取得ドアが閉じたことを確認するデータを取得
                print('data2 = %s'% data2)
                sleep(0.2)
                if data2 <50:
                    print('refgirator door check closed!')
                    GPIO.output(14, GPIO.HIGH)
                    time.sleep(10)
                    #GPIO.output(25, GPIO.HIGH)
                    take_a_picture(picnum)    #保存する写真する名前の数字を新しくする
                    picnum = picnum +1
                    break
                else:
                    GPIO.output(14, GPIO.LOW)
                    print "Refgirator door left open"
        else:
            GPIO.output(14, GPIO.LOW)
            sleep(0.2) 
except KeyboardInterrupt:
    pass

GPIO.cleanup() 
