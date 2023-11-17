import time
from morse import *
import RPi.GPIO as GPIO
import Adafruit_MCP3008


try:


    def led_on_off(pin, value):
        GPIO.output(pin, value)
        
    def switchUserInput(pin): #LED에 불이 들어오면서 동시에 스위치를 이용하여 입력한 문장이 생성됨
        global dotStatus # buttonDot에 대한 전역 변수
        global dashStatus # buttonDash에 대한 전역 변수
        global finStatus # buttonFin에 대한 전역 변수
        
        global ledDot
        global ledDash
        global ledFin

        global switchUserSentence # 스위치를 사용하여 입력한 모스 코드 문장

        if pin == 18: # buttonDot이 눌렸을 때 led가 켜짐
            dotStatus = 0 if dotStatus == 1 else 1
            switchUserSentence += "." # buttonDot이 눌렸을 때 사용자의 입력에 . 을 추가
            led_on_off(ledDot, dotStatus)
        if pin == 23: # buttonDash가 눌렸을 때 led가 켜짐
            dashStatus = 0 if dashStatus == 1 else 1
            switchUserSentence += "-" # buttonDash를 눌렀을 때 사용자의 입력에 - 을 추가
            led_on_off(ledDash, dashStatus)
        if pin == 24: # buttonFin이 눌렸을 때 led가 켜짐
            finStatus = 0 if finStatus == 1 else 1
            switchUserSentence += "n" # buttonFin을 눌렀을 때 사용자의 입력에 n 을 추가
            led_on_off(ledFin, finStatus)

        # switchUserSentence의 맨 마지막과 그 앞 글자가 n인 경우 morseCode 메소드를 호출하여 번역
        if switchUserSentence.strip()[-1] == "n" and switchUserSentence.strip()[-2] == "n":
            sentence = morseCode(switchUserSentence)
            switchUserSentence = "" # 문장 초기화
            return sentence # 변환된 문장을 리턴 - 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
        else:
            switchUserSentence = ""
            return "Wrong Input" # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
    
    def cdsUserInput(signalTime): # 조도 센서를 사용하여 문장 입력
        global cdsUserSentence # 조도 센서를 사용하여 입력한 모스 코드 문장
        global cdsUserStatus # cds사용자가 입력 중인지 아닌지 판단하는 변수
        if signalTime < 0.15: # 조도 센서가 측정한 시간이 0.15초 미만일 때
            cdsUserSentence += "." # . 추가
        elif 0.15 < signalTime < 0.45: # 조도 센서가 측정한 시간이 0.15~0.45초일 때
            cdsUserSentence += "-" # - 추가
        elif 0.45 < signalTime < 0.6: # 조도 센서가 측정한 시간이 0.45~0.6초일 때
            cdsUserSentence += "n" # n 추가
        elif signalTime >= 1.5: # 측정 시간이 1.5초를 넘어갔을 때
            # cdsUserSentence의 맨 마지막과 그 앞 글자가 n인 경우 morseCode 메소드를 호출하여 번역
            if cdsUserSentence.strip()[-1] == "n" and cdsUserSentence.strip()[-2] == "n":
                sentence = morseCode(cdsUserSentence)
                cdsUserSentence = "" # 문장 초기화
                cdsUserStatus = False
                return sentence # 번역 # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
            elif cdsUserSentence.strip()[-1] == "n" and cdsUserSentence.strip()[-2] != "n":
                cdsUserSentence += "n" # 맨 마지막이 n인데 1.5초가 넘어간 경우 사용자의 실수로 간주하여 n을 추가하고 번역
                sentence = morseCode(cdsUserSentence)
                cdsUserSentence = "" # 문장 초기화
                cdsUserStatus = False
                return sentence # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
            else: # 두 경우 모두 아닌 경우 잘못이 맞다고 판단
                cdsUserSentence = ""
                cdsUserStatus = False
                return "Wrong Input" # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
        # 스위치는 제어하기 편하지만 조도 센서는 제어하기 어려운 것을 고려함.

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

    mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10) # 조도 센서 설정
    light = mcp.read_adc(0)
    cdsUserSentence = ""
    cdsUserStatus = True

    global signalTime
    start = 0 # 조도 센서가 측정을 시작한 시간
    end = 0 # 조도 센서가 측정을 마친 시간
    
    while True:
        GPIO.add_event_detect(buttonDot, GPIO.RISING, switchUserInput, bouncetime=10)
        GPIO.add_event_detect(buttonDash, GPIO.RISING, switchUserInput, bouncetime=10)
        GPIO.add_event_detect(buttonFin, GPIO.RISING, switchUserInput, bouncetime=10)
        
        if light > 100: # 조도 센서의 초기 값은 print(light), sleep(1) 루프로 재측정
            start = time.time() # 초기 값보다 커진 순간의 시간
        else:
            end = time.time() # 초기 값보다 작아진 순간의 시간
        signalTime = end - start # 조도 센서가 측정한 시간
        cdsUserInput(signalTime)

except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    GPIO.cleanup()