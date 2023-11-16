import time
import RPi.GPIO as GPIO

try:
    def led_on_off(pin, value):
        GPIO.output(pin, value)
        
    def button_pressed(pin): #LED에 불이 들어오면서 동시에 스위치를 이용하여 입력한 문장이 생성됨
        global dotStatus # buttonDot에 대한 전역 변수
        global dashStatus # buttonDash에 대한 전역 변수
        global finStatus # buttonFin에 대한 전역 변수
        
        global ledDot
        global ledDash
        global ledFin

        global switchUserSentence # 스위치를 사용하여 입력한 모스 코드 문장

        if pin == 18: # buttonDot이 눌렸을 때 led가 켜짐
            dotStatus = 0 if dotStatus == 1 else 1
            switchUserSentence += "."
            led_on_off(ledDot, dotStatus)
        if pin == 23: # buttonDash가 눌렸을 때 led가 켜짐
            dashStatus = 0 if dashStatus == 1 else 1
            switchUserSentence += "-"
            led_on_off(ledDash, dashStatus)
        if pin == 24: # buttonFin이 눌렸을 때 led가 켜짐
            finStatus = 0 if finStatus == 1 else 1
            switchUserSentence += "n"
            led_on_off(ledFin, finStatus)


    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    dotStatus = 0
    dashStatus = 0
    finStatus = 0
    switchUserSentence = ""

    buttonDot = 18 # . 을 입력하는 스위치
    buttonDash = 23 # - 을 입력하는 스위치
    buttonFin = 24 # 띄어쓰기와 입력의 종료를 알리는 스위치
    GPIO.setup(buttonDot, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(buttonDash, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(buttonFin, GPIO.IN, GPIO.PUD_DOWN)


    ledDot = 17 # . 을 입력하는 LED
    ledDash = 27 # - 을 입력하는 LED
    ledFin = 22 # 입력의 종료를 알리는 LED
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    GPIO.add_event_detect(buttonDot, GPIO.RISING, button_pressed, bouncetime=10)
    GPIO.add_event_detect(buttonDash, GPIO.RISING, button_pressed, bouncetime=10)
    GPIO.add_event_detect(buttonFin, GPIO.RISING, button_pressed, bouncetime=10)
    while True:
        pass
except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    GPIO.cleanup()