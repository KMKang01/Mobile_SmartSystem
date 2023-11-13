import time
import RPi.GPIO as GPIO
import io
import cv2
from PIL import Image, ImageFilter
import paho.mqtt.client as mqtt

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

	trig = 20  # GPIO20
	echo = 16  # GPIO16
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(trig, GPIO.OUT)
	GPIO.setup(echo, GPIO.IN)

	def led_on_off(pin, value):
		GPIO.output(pin, value)

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	led1 = 5
	led2 = 13

	GPIO.setup(led1, GPIO.OUT)
	GPIO.setup(led2, GPIO.OUT)

	status1 = 0 #led1의 디지털 값
	status2 = 0 #led2의 디지털 값
	isObjectIn = False #물체가 들어와있는 상태인지 아닌지를 구분하기 위한 변수	

	broker_ip = "localhost"

	client = mqtt.Client()
	client.connect(broker_ip, 1883) # 1883 포트로 mosquitto에 접속
	client.loop_start() # 메시지 루프를 실행하는 스레드 생성

	# 카메라 객체를 생성하고 촬영한 사진 크기를 640x480으로 설정
	camera = cv2.VideoCapture(0, cv2.CAP_V4L)
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	# 프레임을 임시 저장할 버퍼 개수를 1로 설정
	buffer_size = 1
	camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)

	while True:
		distance = measureDistance(trig, echo)
		time.sleep(0.2)  # 좀 더 정확한 측정을 위해 0.2초간격으로 거리 측정

		if distance <= 20: # 물체와의 거리가 20cm 이내로 들어오는 경우
			status1 = 1 # LED1의 디지털 값을 1로 변경
			if distance <= 10: # 물체와의 거리가 10cm 이내로 들어오는 경우
				status2 = 1 # LED2의 디지털 값을 1로 변경
			else:
				status2 = 0
				isObjectIn = False
		else:
			status1 = 0
			status2 = 0

		led_on_off(led1, status1) # 20cm 이내에 물체가 있는 경우 켜짐
		led_on_off(led2, status2) # 10cm 이내에 물체가 있는 경우 켜짐
		
		for i in range(buffer_size+1):
			ret, frame = camera.read()			

		pilim = Image.fromarray(frame) # 프레임 데이터를 이미지 형태로 변환
		stream = io.BytesIO() # 이미지를 저장할 스트림 버퍼 생성
		pilim.save(stream, 'jpeg') # 프레임을 jpeg 형태로 바꾸어 스트림에 저장
		im_bytes = stream.getvalue() # 바이트 배열로 저장
	
		if (distance <= 10 and isObjectIn == False):
			client.publish("jpeg", im_bytes, qos = 0) # 이미지 전송
			isObjectIn = True

except KeyboardInterrupt:
	print("")
finally:
	camera.release() # 카메라 사용 끝내기
	client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
	client.disconnect()
	GPIO.cleanup()