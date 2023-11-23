import time
from morse import *
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import paho.mqtt.client as mqtt

try:
	def cdsUserInput(): # 조도 센서를 사용하여 문장 입력
		global cdsUserSentence # 조도 센서를 사용하여 입력한 모스 코드 문장
		global count

		if count < 30: # count가 30 미만인 경우는 무시(값이 튄 것으로 간주)
			count = 0
		elif count <= 150: # 조도 센서가 측정한 횟수가 150 이하일 때
			cdsUserSentence += "." # . 추가
		elif 150 < count < 450: # 조도 센서가 측정한 횟수가 150~450일 때
			cdsUserSentence += "-" # - 추가
		elif 450 < count < 750 : # 조도 센서가 측정한 횟수가 450~750일 때
			cdsUserSentence += "n" # n 추가
		elif 750 < count : # 측정 횟수가 750을 넘어갔을 때
        # cdsUserSentence의 맨 마지막이 n, 길이가 2 이상인 경우
			if len(cdsUserSentence)>=2 and cdsUserSentence[-1] == "n":
				if cdsUserSentence[-2] == "n":
					print(cdsUserSentence)
					sentence = morseCode(cdsUserSentence)
					cdsUserSentence = "" # 문장 초기화
					count = 0
					print(join_jamos(sentence)) # MQTT로 보낼 예정
				elif cdsUserSentence[-2] != "n":
					cdsUserSentence += "n" # 맨 마지막이 n인데 1050ms가 넘어간 경우 사용자의 실수로 간주하여 n을 추가하고 번역
					print(cdsUserSentence)
					sentence = morseCode(cdsUserSentence)
					cdsUserSentence = "" # 문장 초기화
					count = 0
					print(join_jamos(sentence)) # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
			else: # 측정 시간이 1050ms를 넘었는데 맨 마지막이 n이 아닌 경우
				print(cdsUserSentence)
				cdsUserSentence = ""
				count = 0
				print("Wrong Input") # 일단 return으로 했는데 나중에 플라스크 앱으로 보낼거임
            	# 스위치는 제어하기 편하지만 조도 센서는 제어하기 어려운 것을 고려함.

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10) # 조도 센서 설정
	cdsUserSentence = ""

	count = 0
	while True:
		light = mcp.read_adc(0) # 조도 센서로부터 값을 받음
		time.sleep(0.001)
		if light >= 500: # 조도 센서가 빛을 받는 기준을 500 이상으로 설정
			count += 1
		if light < 500: #  손전등이 꺼졌을 때
			cdsUserInput()
			if count != 0:
				print(count)
				count = 0
				continue

except KeyboardInterrupt:
    print("Ctrl + C")

finally:
    GPIO.cleanup()
