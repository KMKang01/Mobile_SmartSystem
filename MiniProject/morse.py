import time
import RPi.GPIO as GPIO

try:
    def led_on_off(pin, value):
        GPIO.output(pin, value)
        
    def button_pressed(pin):
        global dot # buttonDot에 대한 전역 변수
        global dash # buttonDash에 대한 전역 변수
        global fin # buttonFin에 대한 전역 변수
        global led1 # ledDot에 대한 전역 변수
        global led2 # ledDash에 대한 전역 변수
        global led3 # ledFin에 대한 전역 변수

        if pin == 18: # buttonDot이 눌렸을 때 led가 켜짐
            dot = 0 if dot == 1 else 1
            led_on_off(ledDot, dot)
        if pin == 23: # buttonDash가 눌렸을 때 led가 켜짐
            dash = 0 if dash == 1 else 1
            led_on_off(ledDash, dash)
        if pin == 24: # buttonFin이 눌렸을 때 led가 켜짐
            fin = 0 if fin == 1 else 1
            led_on_off(ledFin, fin)


    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    dot = 0
    dash = 0
    fin = 0

    buttonDot = 18 # . 을 입력하는 스위치
    buttonDash = 23 # _ 을 입력하는 스위치
    buttonFin = 24 # 입력의 종료를 알리는 스위치
    GPIO.setup(buttonDot, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(buttonDash, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(buttonFin, GPIO.IN, GPIO.PUD_DOWN)


    ledDot = 17 # . 을 입력하는 LED
    ledDash = 27 # _ 을 입력하는 LED
    ledFin = 22 # 입력의 종료를 알리는 LED
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    GPIO.add_event_detect(buttonDot, GPIO.RISING, button_pressed, bouncetime=10)
    GPIO.add_event_detect(buttonDash, GPIO.RISING, button_pressed, bouncetime=10)
    GPIO.add_event_detect(buttonFin, GPIO.RISING, button_pressed, bouncetime=10)

except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    GPIO.cleanup()