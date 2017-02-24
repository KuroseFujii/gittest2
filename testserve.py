#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys

def exit_handler(signal, frame):
  """
  Ctrl+Cが押されたときにデバイスを初期状態に戻して終了する。
  """
  print("\nExit")
  servo.stop()
  GPIO.cleanup()
  sys.exit(0)

# 終了処理用のシグナルハンドラを準備
signal.signal(signal.SIGINT, exit_handler)

GPIO.setmode(GPIO.BCM)

# GPIO 12番を使用 (PWM 0)
GPIO.setup(12, GPIO.OUT)
# 20ms / 50Hzに設定、らしい
servo = GPIO.PWM(12, 50)

# 初期化
servo.start(0.0)

# ChangeDutyCycleに渡す値は 0.0 <= dc <= 100.0
# ……のはずだが、なぜか2から12の間で動作している。
dc = 0.0
while True:
  for dc in range(2, 12, 1):
    servo.ChangeDutyCycle(dc)
    print("dc = %d" % dc)
    time.sleep(0.5)
  for dc in range(12, 2, -1):
    servo.ChangeDutyCycle(dc)
    print("dc = %d" % dc)
    time.sleep(0.5)
