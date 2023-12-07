# 스위치 입력

import json # JSON 문자열 사용
from morse import * # morse 변환 함수
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

global client
client = mqtt.Client()
try:
    def led_on_off(pin, value): # LED 제어 함수
        GPIO.output(pin, value)
        
    def switchUserInput(pin): #LED에 불이 들어오면서 동시에 스위치를 이용하여 입력한 문장이 생성됨
        global switchFinPressedTime # buttonFin이 최소 두 번 이상 눌려야 문장이 끝난 것으로 판단하기 위해 만든 변수        
        global switchUserSentence # 스위치를 사용하여 입력한 모스 코드 문장
        global convertedSentence # 변환된 문장
        global msgFromSwitch # MQTT로 발행하기 위한 JSON문자열

        if pin == 18: # 단음에 해당하는 스위치
            switchUserSentence += "o" # buttonDot이 눌렸을 때 사용자의 입력에 o 추가 (JSON문자열을 파싱할 때 .을 허용하지 않기 때문)
        
        if pin == 23: # 장음에 해당하는 스위치
            switchUserSentence += "-" # buttonDash를 눌렀을 때 사용자의 입력에 - 을 추가
        
        if pin == 24: # 띄어쓰기, 문장 종료(모스 부호 문장에서 n으로 설정)에 해당하는 스위치
            switchFinPressedTime += 1 # n이 두번 눌린 경우 종료임을 알리기 위해 추가한 전역 변수
            switchUserSentence += "n" # buttonFin을 눌렀을 때 사용자의 입력에 n 을 추가
        
        # switchUserSentence의 맨 마지막과 그 앞 글자가 n인 경우 morseCode 메소드를 호출하여 번역
        if switchFinPressedTime >= 2: # n이 두 번 눌린 경우
            if switchUserSentence[-1] == "n": # 모스 문장의 맨 마지막이 n인 경우
                if switchUserSentence[-2] == "n": # 모스 문장의 마지막 글자의 앞 글자가 n인 경우(정상적인 입력)
                    convertedSentence = join_jamos(morseCode(switchUserSentence)) # 
                    data = {
                        "morse" : switchUserSentence,
                        "sentence" : convertedSentence
                    }
                    dataOfSwitch = json.dumps(data)
                    send2MQTT(dataOfSwitch)
                    switchFinPressedTime = 0
                    switchUserSentence = "" # 문장 초기화

    def send2MQTT(param):
        client.publish("switch", param, qos=0)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    switchUserSentence = ""
    switchFinPressedTime = 0
    convertedSentence = ""
    msgFromSwitch = ""

    ledDot = 17 # . LED
    ledDash = 27 # - LED
    ledFin = 22 # &nbsp LED
    GPIO.setup(ledDot, GPIO.OUT)
    GPIO.setup(ledDash, GPIO.OUT)
    GPIO.setup(ledFin, GPIO.OUT)

    buttonDot = 18 # . 을 입력하는 스위치
    buttonDash = 23 # - 을 입력하는 스위치
    buttonFin = 24 # 띄어쓰기와 입력의 종료를 알리는 스위치
    GPIO.setup(buttonDot, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(buttonDash, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(buttonFin, GPIO.IN, GPIO.PUD_DOWN)

    #정확한 측정을 위해 디바운스 시간을 200ms로 지정
    GPIO.add_event_detect(buttonDot, GPIO.RISING, switchUserInput, bouncetime=200)
    GPIO.add_event_detect(buttonDash, GPIO.RISING, switchUserInput, bouncetime=200)
    GPIO.add_event_detect(buttonFin, GPIO.RISING, switchUserInput, bouncetime=200)
        
    ip = "localhost"

    client.connect(ip, 1883)
    client.loop_start()

    while True:
        statusOfDot = GPIO.input(buttonDot)
        statusOfDash = GPIO.input(buttonDash)
        statusOfFin = GPIO.input(buttonFin)
        led_on_off(ledDot, statusOfDot)
        led_on_off(ledDash, statusOfDash)
        led_on_off(ledFin, statusOfFin)

except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()