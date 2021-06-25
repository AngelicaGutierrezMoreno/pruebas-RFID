import RPi.GPIO as GPIO #Importar la biblioteca para controlar los GPIOs
from pirc522 import RFID
import time

GPIO.setmode(GPIO.BOARD) #Se define la numeralización de pines de acuerdo a las de la tarjeta (for GPIO numbering, choose BCM) 
GPIO.setwarnings(False) #Desactivar los mensajes de alerta

rc522 = RFID() #Se instancia la librería

#TAGS:
#[167, 117, 157, 95, 16]
#[166, 228, 184, 248, 2]

#RFID_UID = []

def leer_tag():
    print('Esperando tag que leer...')
    rc522.wait_for_tag() #Esperando que un tag pase por el sensor
    (error, tag_type) = rc522.request() #cuando se lea un chip se recupera la información
    if not error : #Si no hay error
        (error, uid) = rc522.anticoll() #Se limpian las posibles choques entre tarjetas, en caso de que pasen al mismo tiempo
        if not error : #Si se limpia con éxito
            print('El ID encontrado fue : {}'.format(uid)) #Se imprime en la terminar el código del tag
            RFID_UID = format(uid)
            #print(RFID_UID )
            time.sleep(1) #Esperamos un segundo para no leer varias veces la tarjeta
    return RFID_UID
                
def agregar_tag():
    RFID_UID = leer_tag()
    print(str(RFID_UID) + 'agregar')
    pajaroDB = open('/home/pi/ceicah/pajarosdb.txt', 'a+')
    pajaroDB.write(str(RFID_UID) + '\n')
    print('Cargado a DB...')
    pajaroDB.close()
    #print('texto cerrado')
    
def lectura_db():
    pajaroDB = open('/home/pi/ceicah/pajarosdb.txt', 'r')
    print('Leyendo DB...')
    contenido = pajaroDB.read()
    print(contenido)
    pajaroDB.close()
    
def eliminar_tag():
    RFID_UID = leer_tag()
    pajaroDB = open('/home/pi/ceicah/pajarosdb.txt', 'a+')
    print('Buscando id...')
    pajaroDB.seek(0) #iniciar lectura al inicio del txt (a=append siempre se pocisionará al final del txt)
    linea = pajaroDB.read()
    uid = RFID_UID
    s = ''
    for uid in linea:
        print('Tag: ' + str(RFID_UID) + ' encontrado')
        if(s!=linea):
            pajaroDB.write(s)
        time.sleep(10)
    pajaroDB.close()
    return print('Tag: ' + str(RFID_UID) + 'eliminado')
#leer_tag()
#agregar_tag()
#lectura_db()
eliminar_tag()