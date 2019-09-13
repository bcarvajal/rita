# librerias para manejo de carpetas
import os
#from glob import glob
# libreria para reconocimiento de caras
import face_recognition
# libreria para procesamiento de imagen
import cv2
# libreria para manejo vectorial
import numpy as np

class ReconocedorFacial:

# Definimos nuestro capturador
	capturador_video = None

# Estas variables almacenaran los registros de personas conocidas
	personas_conocidas_fotos = []
	personas_conocidas_nombres = []

	# Variables para reconocimiento
	ubicacion_caras = []
	caras_detectadas = []
	personas_detectados = []

	# Variable para control de cuadros
	procesar_este_cuadro = True

	on_face_recognized = None

	def __init__(self, webcam):

		# La webcam puede ser una URL http o rtsp
		# Para usar una webcam local dejar como 0
		# Si se tiene mas de una webcam en el pc, incrementar en 1

		video_webcam = 0

		if webcam != "local":
			video_webcam = webcam

		self.capturador_video = cv2.VideoCapture( video_webcam )

	def registrar_evento(self, evento):
	
		self.on_face_recognized = evento

	def registrar_persona(self, nombre, imagen):

		self.personas_conocidas_nombres.append( nombre )
		self.personas_conocidas_fotos.append( face_recognition.face_encodings( face_recognition.load_image_file( imagen ) )[0] )
# Carpeta donde colocaremos a las personas conocidas
# carpeta_personas_conocidas = "C:/Users/LABORATORIO/Desktop/RITA/personas_conocidas"

# Revisaremos las subcarpetas y registraremos los nombres y fotos de cada persona
# for carpeta_persona in os.scandir( carpeta_personas_conocidas ):

	# persona_nombre = os.path.basename( carpeta_persona )
	# persona_fotos = glob( os.path.join(carpeta_persona, "*.jpg") ) + glob( os.path.join(carpeta_persona, "*.jpeg") ) + glob( os.path.join(carpeta_persona, "*.png") )

	# print("")
	# print("Registrando persona: " + persona_nombre)

	# for foto in persona_fotos:

		# print("Agregando foto: " + str(foto))
		# self.personas_conocidas_nombres.append( persona_nombre )
		# self.personas_conocidas_fotos.append( face_recognition.face_encodings( face_recognition.load_image_file( str(foto) ) )[0] )

	def comenzar(self):

	# Bucle principal
		while True:

			# Leemos el cuadro actual
			ret, frame = self.capturador_video.read()

			# Transformamos el cuadro a una matriz RGB (valor numerico 0-255, red green blue)
			matriz_rgb = frame[:, :, ::-1]

			# Verificamos si debemos procesar el cuadro actual o saltarnos al siguiente
			if self.procesar_este_cuadro:

				# Obtenemos la ubicacion de todas las caras detectadas en el cuadro
				self.ubicacion_caras = face_recognition.face_locations(matriz_rgb)
				self.caras_detectadas = face_recognition.face_encodings(matriz_rgb, self.ubicacion_caras)
				self.personas_detectados = []

				# Comparamos las caras detectadas con las caras conocidas
				for cara_detectada in self.caras_detectadas:

					matches = face_recognition.compare_faces(self.personas_conocidas_fotos, cara_detectada)
					nombre_persona = "Desconocido"
					face_distances = face_recognition.face_distance(self.personas_conocidas_fotos, cara_detectada)
					best_match_index = np.argmin(face_distances)
					if matches[best_match_index]:
						nombre_persona = self.personas_conocidas_nombres[best_match_index]
					self.personas_detectados.append(nombre_persona)

			self.procesar_este_cuadro = not self.procesar_este_cuadro

			# Una ves terminado el proceso de deteccion procedemos a
			# dibujar un rectangulo alrededor de las caras detectadas
			for (top, right, bottom, left), nombre_persona in zip(self.ubicacion_caras, self.personas_detectados):

				cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 4)
				cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0,0,255), cv2.FILLED)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, nombre_persona, (left + 6, bottom - 3), font, 0.5, (255,255,255), 1)
				# nombre, arriba, abajo, izquierda, derecha
				
				# callback
				if self.on_face_recognized != None:

					self.on_face_recognized(nombre_persona, top, bottom, right, left)

			# Mostramos el cuadro actual en una ventana
			cv2.imshow('img', frame)

			# Para terminar el programa se debe presionar la letra Q en la ventana del video
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# Terminamos la conexion del capturador de video
		capturador_video.release()

		# Eliminamos la ventana del video
		cv2.destroyAllWindows()
