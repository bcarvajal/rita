import pyttsx3
from nino import ControladorArduino
from momo import ReconocedorFacial

# Establecemos la conexion con el Arduino
arduino = ControladorArduino( puerto="COM8" )

# Definimos nuestro Objeto reconocedor
reconocedor = ReconocedorFacial( webcam="local" )

# Registramos a las personas conocidas
reconocedor.registrar_persona("Marcelo Aros", "marcelo.jpeg")
reconocedor.registrar_persona("Bastian Carvajal", "bastian.jpeg")

# Iniciamos text to speech
voz = pyttsx3.init()
voz.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

ultima_persona = "Nadie"

# Definimos una funcion que sera llamada cuando se encuentre un rostro
def on_cara_detectada(nombre_persona, coordenada_norte, coordenada_sur, coordenada_este, coordenada_oeste):

	global arduino
	global ultima_persona
	global posicion_actual

	if nombre_persona == "Desconocido":

		voz.say("Alerta")
	else:

		if ultima_persona != nombre_persona:
			voz.say("Hola " + nombre_persona)
			ultima_persona = nombre_persona

		# Calculamos el centro de la cara
		x = int( coordenada_oeste + (coordenada_este - coordenada_oeste)/2 )
		y = int( coordenada_norte + (coordenada_sur - coordenada_norte)/2 )

		if x > 426 and x <= 640:

			arduino.mover_camara(16, 0)

		elif x < 213 and x >= 0 :

			arduino.mover_camara(-16, 0)

	voz.runAndWait()

# Enlazamos el evento creado anteriormente a nuestro reconocedor
reconocedor.registrar_evento(on_cara_detectada)

# Iniciamos el reconocimiento
reconocedor.comenzar()