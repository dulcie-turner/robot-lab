#PLC communication file through automation HAT

import time

import automationhat



# sensor 0:temperature 1: pressure 2: acceleration
# 3 digit input 	
def plc_input():
	if automationhat.is_automation_hat():
		automationhat.light.power.write(1)
	sensor = ''
	if automationhat.input[0].read():
		sensor = 'Temperature'
	elif automationhat.input[1].read():
		sensor = 'Pressure'
	elif automationhat.input[2].read():
		sensor = 'Acceleration'
	if sensor != '':
		return sensor
	

# sensor: temperature, pressure, acceleration
# result: pass:1 fail:0
# currently the output is 2-digit for each sensor (probably need to change it)
# output: relay 0: no result; relay 1: has result; output 0: fail; ouput 1: pass
def plc_output(sensor,result):
	if automationhat.is_automation_hat():
		automationhat.light.power.write(1)
	channel = 3
	if sensor == 'Temperature':
		channel = 0
	elif sensor == 'Pressure':
		channel = 1
	elif sensor == 'Acceleration':
		channel = 2
	if channel != 3:
		automationhat.relay[channel].write(1)
		if result == 1:
			automationhat.output[channel].write(1)
		elif result == 0:
			automationhat.output[channel].write(0)
		plc_result = int(str(automationhat.output[channel].read())+str(automationhat.relay[channel].read()))
		print(sensor,plc_result)
		return plc_result


	
while True:
	automationhat.output.write(0)
	automationhat.relay.write(0)
	if plc_input()!= None:
		print(plc_output(plc_input(),0))
		time.sleep(1)
		automationhat.output.write(1)
		automationhat.relay.write(1)
	else:
		continue

	
	
