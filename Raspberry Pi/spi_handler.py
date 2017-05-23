import spidev
import time
import os, sys
SendReques = 0
SendDelay = 1 #TODO only temporary value

def request(req_id):
	resp = spi.xfer([SendReques])
	time.sleep(0.1)
	resp = spi.xfer([req_id])
	return 1

def control(ctrl_id, ctrl_val):
	resp = spi.xfer([ctrl_id])
	time.sleep(0.1)
	resp = spi.xfer([ctrl_val])
	return 1

def init():
	spi = spidev.SpiDev()
	spi.open(0, 1)
	return 1

def deinit():
	resp = spi.xfer([0x00])    
	spi.close()
	return 1
