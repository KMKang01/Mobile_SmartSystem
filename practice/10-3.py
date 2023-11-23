import time
import RPi.GPIO as GPIO
import Adafruit_MCP3008
try:	
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	btn = 24
	GPIO.setup(btn, GPIO.IN, GPIO.PUD_DOWN)

	mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

	start = 0
	end = 0
	isLightON=False

	global count
	count = 0

	while(True):
		light = mcp.read_adc(0)
		time.sleep(0.01)
		if light > 400:
			print(light)
			count += 1
		status = GPIO.input(btn)
		if status == 1:	
			print(count,"번")
			count = 0
			continue

except KeyboardInterrupt:
	print("")
finally:
	GPIO.cleanup()
