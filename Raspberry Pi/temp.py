import RPi.GPIO as GPIO
import time
import spidev
import os, sys
import SpiMaster
import Adafruit_DHT
from flask import request
from flask import Flask, render_template
from flask import json

#Master request from slave:
#byte0 will have 0 value for request commands
#byte1 will have one of the following values
MasterRequests = {
	'GetT1':10, 'GetT2':11, 'GetT3':12, 
	'GetL1':20, 'GetL2':21, 'GetL3':22,
    'GetSF':30, 'GetSS':29
}

#Master control slave:
#byte0 will have on of the following values
MasterCommands = {
	'SetT1':10, 'SetT2':11, 'SetT3':12, 
	'SetV1':15, 'SetV2':16,
	'SetL1Red':20, 'SetL1Green':21, 'SetL1Blue':22,
	'SetL2Red':23, 'SetL2Green':24, 'SetL2Blue':25,
	'SetL3Red':26, 'SetL3Green':27, 'SetL3Blue':28 
}
#byte1 will be the value associated to these commands
#IT IS THE RESPONSIBILITY OF THE MASTER TO SEND VALID VALUES

##################################################

app = Flask(__name__)

@app.route("/")
def index():
   return render_template('main.html')

@app.route("/style.css")
def style():
   return render_template('style.css')

################################################
#                                              #
#    Temperature and Ventilation functions     #
#                                              #
################################################

#Temperature Monitoring
@app.route("/temperature_monitoring", methods=['GET'])
def GetTemp():
	t1 = 0 #sensor1
	t2 = 0 #sensor2
	t3 = 0 #sensor3
	
	t1 = SpiMaster.request(MasterRequests['GetT1']);
	time.sleep(0.1)
	t2 = SpiMaster.request(MasterRequests['GetT2']);
	time.sleep(0.1)
	t3 = SpiMaster.request(MasterRequests['GetT3']);
	
	data = {'t1Monitor': t1[1], 't2Monitor': t2[1], 't3Monitor': t3[1]};

	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response	

#Function for T1 temperature setting
@app.route('/t1_temp_control', methods=['POST'])
def SetT1Temp():
	t1 = request.form.get('t1Control')
	t1 = int(t1)
	if(t1>=0)&(t1<=40):
		SpiMaster.control(MasterCommands['SetT1'],t1)
		response = 'OK'
	else:
		response = 'FAIL'

	data={'response':response, 't1Control':t1};
	
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

#Function for T2 temperature setting
@app.route('/t2_temp_control', methods=['POST'])
def SetT2Temp():
	t2 = request.form.get('t2Control')
	t2 = int(t2)
	if(t2>=0)&(t2<=40):
		SpiMaster.control(MasterCommands['SetT2'],t2)
		response = 'OK'
	else:
		response = 'FAIL'

	data={'response':response, 't2Control':t2};
	
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

#Function for T3 temperature setting
@app.route('/t3_temp_control', methods=['POST'])
def SetT3Temp():
	t3 = request.form.get('t3Control')
	t3 = int(t3)
	if(t3>=0)&(t3<=40):
		SpiMaster.control(MasterCommands['SetT3'],t3)
		response = 'OK'
	else:
		response = 'FAIL'

	data={'response':response, 't3Control':t3};
	
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

# FUNCTION FOR TEMPERATURE & HUMIDITY
@app.route("/sensor_DHT11", methods=['GET'])
def TempHumMonitor():
	sensor_pin = 4
	sensor_type = Adafruit_DHT.DHT11
	temperature = 0
	humidity = 0
	humidity, temperature = Adafruit_DHT.read_retry(sensor_type, sensor_pin)
	temperature = int(temperature)
	humidity = int(humidity)
	print "Temperature is: ", temperature
	print "Humidity is: ", humidity
	data={'temperature': temperature, 'humidity': humidity};
	
	print "data is", data
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response	

#Function for main ventilation setting
@app.route('/main_vent_setting', methods=['POST'])
def SetMainVent():
	v1 = request.form.get('v1Control')
	v1 = int(v1)
	SpiMaster.control(MasterCommands['SetV1'],v1)
	data={'v1Control':v1};
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

#Function for secondary ventilation setting
@app.route('/secondary_vent_setting', methods=['POST'])
def SetSecondaryVent():
	v2 = request.form.get('v2Control')
	v2 = int(v2)
	SpiMaster.control(MasterCommands['SetV2'],v2)
	data={'v2Control':v2};
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

################################################
#                                              #
#            Lightenining functions            #
#                                              #
################################################

#Lightenining Monitoring
@app.route("/light_monitoring", methods=['GET'])
def GetLight():
	l1 = 0 #sensor1
	l2 = 0 #sensor2
	l3 = 0 #sensor3
	
	l1 = SpiMaster.request(MasterRequests['GetL1']);
	l2 = SpiMaster.request(MasterRequests['GetL2']);
	l3 = SpiMaster.request(MasterRequests['GetL3']);
	
	data = {'l1Monitor': l1[1], 'l2Monitor': l2[1], 'l3Monitor': l3[1]};

	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response	

#Function for L1 lightening setting
@app.route('/l1_light_control', methods=['POST'])
def SetL1Light():
	l1r = request.form.get('l1Red')
	l1g = request.form.get('l1Green')
	l1b = request.form.get('l1Blue')
	l1r = int(l1r)
	l1g = int(l1g)
	l1b = int(l1b)

	SpiMaster.control(MasterCommands['SetL1Red'],l1r)
	SpiMaster.control(MasterCommands['SetL1Green'],l1g)
	SpiMaster.control(MasterCommands['SetL1Blue'],l1b)

	data={'l1Red':l1r, 'l1Green':l1g, 'l1Blue':l1b};
	
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

#Function for L2 lightening setting
@app.route('/l2_light_control', methods=['POST'])
def SetL2Light():
	l2r = request.form.get('l2Red')
	l2g = request.form.get('l2Green')
	l2b = request.form.get('l2Blue')
	l2r = int(l2r)
	l2g = int(l2g)
	l2b = int(l2b)
	SpiMaster.control(MasterCommands['SetL2Red'],l2r)
	SpiMaster.control(MasterCommands['SetL2Green'],l2g)
	SpiMaster.control(MasterCommands['SetL2Blue'],l2b)
	data={'l2Red':l2r, 'l2Green':l2g, 'l2Blue':l2b};
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

#Function for L3 lightening setting
@app.route('/l3_light_control', methods=['POST'])
def SetL3Light():
	l3r = request.form.get('l3Red')
	l3g = request.form.get('l3Green')
	l3b = request.form.get('l3Blue')
	l3r = int(l3r)
	l3g = int(l3g)
	l3b = int(l3b)
	SpiMaster.control(MasterCommands['SetL3Red'],l3r)
	SpiMaster.control(MasterCommands['SetL3Green'],l3g)
	SpiMaster.control(MasterCommands['SetL3Blue'],l3b)
	data={'l3Red':l3r, 'l3Green':l3g, 'l3Blue':l3b};
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response


################################################
#                                              #
#            Serial Debug functions            #
#                                              #
################################################

#Send Serial Message
@app.route('/send_spi_message', methods=['POST'])
def SendSpiDebugMessage():
	global SerialDebugResponse
	print "SendSpiDebugMessage function entered..."
	send_delay = 2 #use such a large value only for tesing with shift register, final walue will have to be much smaller!!!
	varSpiByte0 = request.form.get('sendSpiByte0')
	varSpiByte0 = int(varSpiByte0)
	varSpiByte1 = request.form.get('sendSpiByte1')
	varSpiByte1 = int(varSpiByte1)
	if(varSpiByte0>=0)&(varSpiByte0<=255)&(varSpiByte1>=0)&(varSpiByte1<=255):
		#valid input detected
		SerialDebugResponse = SpiMaster.control(varSpiByte0,varSpiByte1)
	data={'sendSpiByte0':varSpiByte0,'sendSpiByte1':varSpiByte1,'receiveSpiByte0':SerialDebugResponse[0],'receiveSpiByte1':SerialDebugResponse[1],'receiveCrc':SerialDebugResponse[2]};

	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response

#Receive Serial Message
@app.route('/receive_spi_message', methods=['GET'])
def ReceiveSpiDebugMessage():
	print "ReceiveSpiDebugMessage function entered..."
	global SerialDebugResponse
	print "Spi response is: ", SerialDebugResponse

	data={'receiveSpiByte0':SerialDebugResponse[0],'receiveSpiByte1':SerialDebugResponse[1],'receiveCrc':SerialDebugResponse[2]};
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response


################################################
#                                              #
#    Security functions                        #
#                                              #
################################################

# Security Monitoring
@app.route("/security_monitoring", methods=['GET'])
def GetSecurity():
	s1 = 0 #sensor1 security
	s2 = 0 #sensor2 security

	
	s1 = SpiMaster.request(MasterRequests['GetSS']);
	time.sleep(0.1)
	s2 = SpiMaster.request(MasterRequests['GetSF']);

	
	data = {'s1MonitorSecurity': s1[1], 's2MonitorFlood': s2[1]};
	
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response	

#######################################################################

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
SpiMaster.init()

try:
	if __name__ == "__main__":
		app.run(host='0.0.0.0', port=8080, debug=True)
	while True:
		print "1"
except KeyboardInterrupt:
	SpiMaster.deinit()
	print "GPIO Cleanup..."
	GPIO.cleanup()
	print "Closing Server..."
#ajunge aici dupa ce opresti server-ul
