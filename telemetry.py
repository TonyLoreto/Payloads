#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import serial,time
import socket
import sys
import re
import select

#MPU
from mpu6050 import mpu6050

mpu = mpu6050(0x68)
UDP_IP="0.0.0.0" # Recibir de cualquier cliente
#UDP_PORT=10000
print("Ingresa el puerto XXXXX")
UDP_PORT= int(input())

UDP_HOST = sys.argv[1]
# UDP_HOST ='192.168.1.0' 
print ("Conectar a %s" % UDP_HOST)

sock = socket.socket( socket.AF_INET, # Internet
socket.SOCK_DGRAM ) # UDP

sock.bind( (UDP_IP,UDP_PORT) )

ser=serial.Serial("/dev/ttyS0", baudrate=115200) #ttyAMC0
# Pone el socket en modo de no bloqueo,
# evitando poner a recv en bucle infinito si no hay datos en el buffer
sock.setblocking(0)

while True:
    
    temp_data = mpu.get_temp()
    temp=str(temp_data)
    accel_data = mpu.get_accel_data()
    accel=str(accel_data)
    gyro_data = mpu.get_gyro_data()
    gyro=str(gyro_data)

    # print("Temp : "+str(mpu.get_temp()))
    # print("Acc X : "+str(accel_data['x']))
    # print("Acc Y : "+str(accel_data['y']))
    # print("Acc Z : "+str(accel_data['z']))
    # print("Gyro X : "+str(gyro_data['x']))
    # print("Gyro Y : "+str(gyro_data['y']))
    # print("Gyro Z : "+str(gyro_data['z']))

    sock.sendto(temp.encode('utf8'), (UDP_HOST, UDP_PORT))
    sock.sendto(accel.encode('utf8'), (UDP_HOST, UDP_PORT))
    sock.sendto(gyro.encode('utf8'), (UDP_HOST, UDP_PORT))
    time.sleep(1)
    # if HayDatosTeclado[0]:
        # mensaje = sys.stdin.readline()
        # print("Mensaje para remoto:", mensaje)
        # sock.sendto(mensaje.encode('utf8'), (UDP_HOST, UDP_PORT))
        # # Valida si recibe algo por el socket
    HayDatosSocket = select.select([sock],[],[],0.5)
    if HayDatosSocket[0]:
        Socketdata = sock.recv( 1024 ) # buffer size is 1024 bytes 
        pass
        HayDatosTeclado = []
        HayDatosSocket = []
