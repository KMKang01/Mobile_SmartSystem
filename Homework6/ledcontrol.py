import time
import RPi.GPIO as GPIO

try:
	def measureDistance(trig, echo):
		GPIO.output(trig, 1)  # tr
		GPIO.output(trig, 0)  # trig 핀 신호 High->Low. 초음사 발사 지시

		while GPIO.input(echo) == 0:  # echo 핀 값이 1로 바뀔때까지 루프
			pass

        # echo 핀 값이 1이면 초음파가 발사되었음
		pulse_start = time.time()  # 초음파 발사 시간 기록
		while GPIO.input(echo) == 1:  # echo 핀 값이 0이 될때까지 루프
			pass

        # echo 핀 값이 0이 되면 초음파 수신하였음
		pulse_end = time.time()  # 초음파가 되돌아 온 시간 기록
		pulse_duration = pulse_end - pulse_start  # 경과 시간 계산
		return pulse_duration * 340 * 100 / 2  # 거리 계산하여 리턴(단위 cm)


	def led_on_off(pin, value):
		GPIO.output(pin, value) # LED의 동작 제어 함수

	trig = 20 #GPIO20
	echo = 16 #GPIO16
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(trig, GPIO.OUT)
	GPIO.setup(echo, GPIO.IN)

	led1 = 5
	led2 = 13

	GPIO.setup(led1, GPIO.OUT)
	GPIO.setup(led2, GPIO.OUT)

	status1 = 0 #LED 1번의 디지털 값
	status2 = 0 #LED 2번의 디지털 값
	
	while True:
		distance = measureDistance(trig, echo)
		time.sleep(0.2)  # 좀 더 정확한 측정을 위해 0.2초으로 거리 측정

		if distance <= 20: # 물체와의 거리가 20cm 이내로 들어오는 경우
			status1 = 1 # LED1의 디지털 값을 1로 변경
			if distance <= 10: # 물체와의 거리가 10cm 이내로 들어오는 경우
				status2 = 1 # LED2의 디지털 값을 1로 변경
			else: # 물체와의 거리가 10cm를 벗어난 경우
				status2 = 0 # LED2의 디지털 값을 0으로 변경
		else: # 물체와의 거리가 20cm를 벗어난 경우
			status1 = 0 # LED1의 디지털 값을 0으로 변경
			status2 = 0

		led_on_off(led1, status1) # 20cm 이내에 물체가 있는 경우 켜짐
		led_on_off(led2, status2) # 10cm 이내에 물체가 있는 경우 켜짐

except KeyboardInterrupt:
    print("Ctrl+C")
finally:
    GPIO.cleanup()
