#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import smbus
import time
import socket
import sys
import select
#Configuracion UDP

UDP_IP="0.0.0.0" # Recibir de cualquier cliente
#UDP_PORT=10000
#print("Ingresa el puerto XXXXX")
# UDP_PORT= int(input())
UDP_PORT= 1111
# UDP_HOST = sys.argv[1]
UDP_HOST = "192.168.50.1" 
print ("Conectar a %s:%s" %(UDP_HOST,UDP_PORT) )

sock = socket.socket( socket.AF_INET, # Internet
socket.SOCK_DGRAM ) # UDP

sock.bind( (UDP_IP,UDP_PORT) )

# Pone el socket en modo de no bloqueo,
# evitando poner a recv en bucle infinito si no hay datos en el buffer
sock.setblocking(0)

print("Estableciendo la conexion...")
sock.sendto(b"Starting socket UDP", (UDP_HOST, UDP_PORT))
print ("Conexion establecida")
# for RPI version 1, use bus = smbus.SMBus(0)

#Configuracion i2c

bus = smbus.SMBus(1)
 
# This is the address we setup in the Arduino Program
address = 0x07
 
def writeData(value):
    byteValue = StringToBytes(value)    
    bus.write_i2c_block_data(address,0x00,byteValue) #first byte is 0=command byte.. just is.
    return -1
 
 
def StringToBytes(val):
        retVal = []
        for c in val:
                retVal.append(ord(c))
        return retVal
 
while True:
    HayDatosSocket = select.select([sock],[],[],0.5)
    if HayDatosSocket[0]:
        Socketdata = sock.recv( 1024 ) # Buffer de 1024 bytes de tamao 
        Realdata=Socketdata[:-1].encode(encoding='ascii', errors='strict')
        print ("mensaje Recibido:", Realdata)
        # print (len(Realdata))
        writeData(Realdata)
        time.sleep(.1)
        writeData("0,0")
        HayDatosSocket = []
