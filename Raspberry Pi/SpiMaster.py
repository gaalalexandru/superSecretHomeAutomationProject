import spidev
import time
import os, sys
SendRequest = 0
SendDelay = 0.1 #TODO only temporary value
global spi

def request(req_id):
	global spi
	crc_check = 0 #variable to check crc content
	req_id_check = 0 #variable to check control id response
	retry_counter = 2 #try to resend retry_counter nr of times the message if conditions are not furfilled
	req_crc = req_id ^ SendRequest
	retry = 1
	
	while ((crc_check == 0)|(req_id_check == 0))&(retry_counter != 0):
		#response = spi.xfer2([SendRequest,req_id,req_crc]) #send data and receive response
		spi.writebytes([SendRequest,req_id,req_crc])
		print "spi write"
		time.sleep(0.05)
		response = spi.readbytes(3)
		print "spi read"
		if ((response[0] ^ response[1]) == response[2]):
			crc_check = 1 #acknowledge received CRC
		if (response[0] == req_id):
			req_id_check = 1 #acknowledge received request response
		retry_counter = retry_counter - 1
		print "Try nr: ", retry, " with response: ",response
		retry = retry + 1
		time.sleep(0.1)

	print "Request ID: ", req_id
	print "Control CRC: ", req_crc	
	print "Response: ", response
	return response

def control(ctrl_id, ctrl_val):
	global spi
	crc_check = 0 #variable to check crc content
	ctrl_id_check = 0 #variable to check control id response
	retry_counter = 2 #try to resend retry_counter nr of times the message if conditions are not furfilled
	ctrl_crc = ctrl_id ^ ctrl_val
	retry = 1
	#response=[-1,-1,-1]
	while ((crc_check == 0)|(ctrl_id_check == 0))&(retry_counter != 0):
		#response = spi.xfer2([ctrl_id,ctrl_val,ctrl_crc])
		spi.writebytes([ctrl_id,ctrl_val,ctrl_crc])
		print "spi write"
		time.sleep(0.05)
		response = spi.readbytes(3)
		print "spi read"
		if ((response[0] ^ response[1]) == response[2]):
			crc_check == 1 #acknowledge received CRC
		if (response[0] == ctrl_id):
			ctrl_id_check = 1 #acknowledge received request response
		retry_counter = retry_counter - 1
		print "Try nr: ", retry, " with response: ",response
		retry = retry + 1
		time.sleep(0.1)

	print "Control ID: ", ctrl_id
	print "Control Value: ", ctrl_val
	print "Control CRC: ", ctrl_crc	
	print "Response: ", response
	return response

def init():
	global spi
	spi = spidev.SpiDev()
	spi.open(0,1)
	spi.max_speed_hz = 6666666
	spi.mode = 1
	spi.bits_per_word = 8
	print "SPI initialized"
	return 1

def deinit():
	global spi
	resp = spi.xfer([0x00])    
	spi.close()
	print "SPI de-initialized"
	return 1
