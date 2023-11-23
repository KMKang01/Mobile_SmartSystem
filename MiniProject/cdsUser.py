import time
from morse import *
import RPi.GPIO as GPIO
import Adafruit_MCP3008

try:
    def cdsUserInput(duration): # 조도 센서를 사용하여 문장 입력
        global cdsUserSentence # 조도 센서를 사용하여 입력한 모스 코드 문장
        global isCdsOn # 조도 센서로 값을 받고 있는지 확인

        if duration <= 0.2: # 조도 센서가 측정한 시간이 0.15초 미만일 때
            cdsUserSentence += "." # . 추가
        elif 0.2 < duration < 0.5: # 조도 센서가 측정한 시간이 0.2~0.6초일 때
            cdsUserSentence += "-" # - 추가
        elif 0.5 < duration < 1.0: # 조도 센서가 측정한 시간이 0.6~1.0초일 때
            cdsUserSentence += "n" # n 추가
        elif duration >= 1.5: # 측정 시간이 1.5초를 넘어갔을 때
            # cdsUserSentence의 맨 마지막과 그 앞 글자가 n인 경우 morseCode 메소드를 호출하여 번역
            if cdsUserSentence[-1] == "n":
                if cdsUserSentence[-2] == "n":
                    sentence = morseCode(cdsUserSentence)
                    cdsUserSentence = "" # 문장 초기화
                    print(sentence) # 번역 # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
                
                elif cdsUserSentence[-2] != "n":
                    cdsUserSentence += "n" # 맨 마지막이 n인데 1.5초가 넘어간 경우 사용자의 실수로 간주하여 n을 추가하고 번역
                    sentence = morseCode(cdsUserSentence)
                    cdsUserSentence = "" # 문장 초기화
                    print(sentence) # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
                
            else: # 두 경우 모두 아닌 경우 잘못이 맞다고 판단
                cdsUserSentence = ""
                print("Wrong Input") # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
        # 스위치는 제어하기 편하지만 조도 센서는 제어하기 어려운 것을 고려함.

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10) # 조도 센서 설정
    cdsUserSentence = ""
    isCdsOn = False
    
    global signalTime
    start = 0 # 조도 센서가 측정을 시작한 시간
    end = 0 # 조도 센서가 측정을 마친 시간
    
    while True:
        light = mcp.read_adc(0) # 조도 센서로부터 값을 받음
        time.sleep(0.01)
        if light >= 400: # 조도 센서의 기본 값 경계가 300 언저리이므로 손전등을 비췄을 때를 500 이상으로 설정
            start = time.time() # 초기 값보다 커진 순간의 시간
            isCdsOn = True # 조도 센서로부터 값을 받아 시간 측정을 하고 있음을 알려주는 변수
        if isCdsOn == True and light < 400: # 손전등이 꺼졌을 때
            end = time.time() # 기준 값보다 작아진 순간의 시간
            isCdsOn = False # 시간 측정이 끝났음을 알려주는 변수
            signalTime = end - start # 조도 센서가 측정한 시간
            cdsUserInput(signalTime)

except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    GPIO.cleanup()