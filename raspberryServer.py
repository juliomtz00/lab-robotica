# CODIGO RASPBERRY

import time
import socket
import network
from machine import Pin, PWM
from controlL298N import DCmotores

ssid = 'Equipo3-Network'
password = 'ROBOT4103'


spdAng = 55
spdFwd = 55

motorRRP = Pin(1, Pin.OUT)
motorRRN = Pin(2, Pin.OUT)
motorRLP = Pin(4, Pin.OUT)
motorRLN = Pin(5, Pin.OUT)
motorFRP = Pin(16, Pin.OUT)
motorFRN = Pin(17, Pin.OUT)
motorFLP = Pin(19, Pin.OUT)
motorFLN = Pin(20, Pin.OUT)
enableRR = PWM(Pin(0))
enableRL = PWM(Pin(3))
enableFR = PWM(Pin(15))
enableFL = PWM(Pin(18))
motores = DCmotores(motorRRP, motorRRN, motorRLP, motorRLN, motorFRP, motorFRN, motorFLP, motorFLN, enableRR, enableRL, enableFR, enableFL)
motores.stop()


ap = network.WLAN(network.AP_IF)
ap.config(essid = ssid, password = password)
ap.active(True)

while ap.active() == False:
    pass

print('Connection successful')
status = ap.ifconfig()
print(status)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(1)


print('\nESPERANDO CONEXION A LA RED, %s...' % str(ssid))
conn, addr = s.accept()
print('Got a connection from %s' % str(addr[0]))

addrss = ''
try:
    print('\n')
    # https://docs.micropython.org/en/latest/library/network.html
    # WiFi AP: use 'stations' to retrieve a list of all the STAs connected to the AP.
    # The list contains tuples of the form (MAC, RSSI).
    stat = ap.status('stations') # Regresa un tuple[(MAC, RSSI)]
    lista = list(stat[0]) # Se convierte el primer elemento del tuple en lista
    # Se convierte la lista en formato legible de MAC address (BSSID)
    addrss = lista[0].hex(":")
    print('STATUS, CLIENT BSSID: ', addrss)
except:
    # Cuando se corra la primera vez el codigo arrojara esta leyenda, por lo cual se
    # debera detener la corrida, conectarse a la red que se establecio mas arriba en 
    # este mismo codigo, en este caso 'Equipo3-Network', y volver a correr el codigo
    # LA PRIMERA CORRIDA ACTIVA LA RED Wi-Fi DEL SERVIDOR
    print('NO CLIENT CONNECTED')


while True:
    recvData, address = conn.recvfrom(1024)
    dataPrint = recvData.decode('utf-8')
    while dataPrint != '0':
        if dataPrint == '1':
            motores.turnClockwise(spdAng)
        elif dataPrint == '2':
            motores.turnCounterClockwise(spdAng)
        elif dataPrint == '3':
            motores.forward(spdFwd)
        recvData, address = conn.recvfrom(1024)
        dataPrint = recvData.decode('utf-8')
    if dataPrint == '0':
        motores.stop()


