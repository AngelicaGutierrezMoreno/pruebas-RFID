
#El sensor debe esperar 5 seg

import RPi.GPIO as GPIO #Importar la biblioteca para controlar los GPIOs
from pirc522 import RFID
import time

GPIO.setmode(GPIO.BOARD) #Se define la numeralización de pines de acuerdo a las de la tarjeta (for GPIO numbering, choose BCM) 
GPIO.setwarnings(False) #Desactivar los mensajes de alerta

rc522 = RFID() #Se instancia la librería

class Tag:
    # instance attributes
    def __init__(self):
        self.__tag_leido = []
    
    #getter
    def getTag(self):
        return self.__tag_leido
        
    #setter
    def setTag(self, tag):
        self.__tag_leido = tag
        
         
def leer_tag():
    print('Cargando...')
    time.sleep(1)
    print('Pase el tag por sensor...')
    rc522.wait_for_tag() #Esperando que un tag pase por el sensor
    (error, tag_type) = rc522.request() #cuando se lea un chip se recupera la información
    if not error : #Si no hay error
        (error, uid) = rc522.anticoll() #Se limpian las posibles choques entre tarjetas, en caso de que pasen al mismo tiempo
        if not error : #Si se limpia con éxito
            #print('El ID encontrado fue : {}'.format(uid)) #Se imprime en la terminar el código del tag
            tag.setTag(format(uid))
            tag.getTag()
            print('El tag es: {}' .format(tag.getTag()))
            #print(RFID_UID )
            time.sleep(1) #Esperamos un segundo para no leer varias veces la tarjeta

def agregar_tag():
    tarjeta = tag.getTag()
    pajaroDB = open('/home/pi/ceicah/pajarosdb.txt', 'a+')
    pajaroDB.write(str(tarjeta) + '\n')
    print('Cargado a DB...')
    pajaroDB.close()
    #print('texto cerrado')
    
def lectura_db():
    pajaroDB = open('/home/pi/ceicah/pajarosdb.txt', 'r')
    print('Leyendo DB...')
    contenido = pajaroDB.read()
    print(contenido)
    pajaroDB.close()
 
def validar_tag():
    tarjeta = tag.getTag()
    pajaroDB = open('/home/pi/ceicah/pajarosdb.txt', 'a+')
    print('Buscando id...')
    pajaroDB.seek(0) #iniciar lectura al inicio del txt (a=append siempre se pocisionará al final del txt)
    linea = pajaroDB.read()
    if tarjeta in linea:
        print('Tag: ' + str(tarjeta) + ' encontrado')
    else:
        print('Nel, siga participando')
    time.sleep(1)
    pajaroDB.close()
    
def nocopy_tag():
#     time.sleep(5)
    tarjeta = tag.getTag()
    pajaroDB = open('/home/pi/ceicah/pajarosdb.txt', 'r')
    print('Leyendo DB...')
    pajaroDB.seek(0) #iniciar lectura al inicio del txt (a=append siempre se pocisionará al final del txt)
    linea = pajaroDB.read()
    if str(tarjeta) in linea:
        print('El tag ya estaba registrado')
    else:
        agregar_tag()
        print('Tag: ' + '{}'.format(tag.getTag()) + ' agregado')
    time.sleep(1)
    pajaroDB.close()

tag = Tag()
leer_tag()
#agregar_tag()
nocopy_tag()
#lectura_db()
#validar_tag()