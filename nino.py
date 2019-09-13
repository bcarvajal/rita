# @autor: Bastian Carvajal
# PD: nino best gotoubun

import serial
import time

class ControladorArduino:

	speed = 9600
	conexion = None
	posicionX = 320
	posicionY = 240

	def __init__(self, puerto):

		self.conexion = serial.Serial(puerto, self.speed, timeout=0)
		time.sleep(3)
		self.mover_camara( 0, 0 )

	def mover_camara(self, x, y):

		self.posicionX += x
		self.posicionY += y

		#X{0:d}Y{1:d}Z
		self.conexion.write( "X{0:d}Y".format(self.posicionX, self.posicionY).encode()  )