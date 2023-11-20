import time
from morse import *
import RPi.GPIO as GPIO

try:
    def led_on_off(pin, value):
        GPIO.output(pin, value)
        
    def switchUserInput(pin): #LED에 불이 들어오면서 동시에 스위치를 이용하여 입력한 문장이 생성됨
        global switchFinPressedTime # buttonFin이 최소 두 번 이상 눌려야 문장이 끝난 것으로 판단하기 위해 만든 변수        
        global switchUserSentence # 스위치를 사용하여 입력한 모스 코드 문장

        if pin == 18:
            switchUserSentence += "." # buttonDot이 눌렸을 때 사용자의 입력에 . 을 추가
            print(switchUserSentence)
        
        if pin == 23:
            switchUserSentence += "-" # buttonDash를 눌렀을 때 사용자의 입력에 - 을 추가
            print(switchUserSentence)
        
        if pin == 24:
            switchFinPressedTime += 1
            switchUserSentence += "n" # buttonFin을 눌렀을 때 사용자의 입력에 n 을 추가
            print(switchUserSentence)
        
        # switchUserSentence의 맨 마지막과 그 앞 글자가 n인 경우 morseCode 메소드를 호출하여 번역
        if switchFinPressedTime >= 2:
            if switchUserSentence[-1] == "n":
                if switchUserSentence[-2] == "n":
                    sentence = morseCode(switchUserSentence)
                    switchFinPressedTime = 0
                    switchUserSentence = "" # 문장 초기화
                    print(sentence) # 변환된 문장을 리턴 - 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    switchUserSentence = ""
    switchFinPressedTime = 0
    
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
    GPIO.add_event_detect(buttonDot, GPIO.RISING)
    GPIO.add_event_detect(buttonDash, GPIO.RISING)
    GPIO.add_event_detect(buttonFin, GPIO.RISING)

    while True:
        statusOfDot = GPIO.input(buttonDot)
        statusOfDash = GPIO.input(buttonDash)
        statusOfFin = GPIO.input(buttonFin)
        led_on_off(ledDot, statusOfDot)
        led_on_off(ledDash, statusOfDash)
        led_on_off(ledFin, statusOfFin)
      
        if(GPIO.event_detected(buttonDot)):
            time.sleep(0.005)
            switchUserInput(buttonDot)
        if(GPIO.event_detected(buttonDash)):
            time.sleep(0.005)
            switchUserInput(buttonDash)
        if(GPIO.event_detected(buttonFin)):
            time.sleep(0.005)
            switchUserInput(buttonFin)
        
except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    GPIO.cleanup()
