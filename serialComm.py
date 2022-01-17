#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 17:29:33 2021

"""

import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo 
import io
import time
from struct import *

class serialComm():
    Devices = []
    PrevDevice = None
    Device = None
    Indicator = ""
    
    def __init__(self):
        self.Device = None
        self.PrevDevice = None
    
    def findPacemaker(self):
        devList = serial.tools.list_ports.comports()
        for i in range(0,len(devList)):
            if devList[i].vid is not None and devList[i].pid is not None:
                #Isolate Packemaker devices from rest
                if(('{:#06x}'.format(devList[i].vid) == '0x1366') and ('{:#06x}'.format(devList[i].pid) == '0x1015')):
                    return devList[i]
    
    def setDevice(self):
        self.Device = self.findPacemaker()
        
    def deviceStatus(self):
        foundDev = self.findPacemaker()
        #print("MY DEVICE SEARCH")
        
        if(foundDev != self.Device):
            #print("Change in Device")
            if((foundDev not in serialComm.Devices) and (foundDev != None)):     #New Device
                serialComm.Devices.append(foundDev)
                if(self.PrevDevice != None):
                    self.PrevDevice = self.Device
                self.Device = foundDev
                serialComm.Indicator = "New Device Connected"
                #statusChange = True
                
            elif((foundDev != self.PrevDevice) and (foundDev != None)):     #Old device, but not same as last interogated
                serialComm.Indicator = "Device Connected: Different From Last Device"
                if(foundDev != self.PrevDevice):
                    self.PrevDevice = self.Device
                self.Device = foundDev
                
            elif((foundDev == self.PrevDevice) and (foundDev != None)):
                serialComm.Indicator = "Device Connected"
                if(foundDev != self.PrevDevice):
                    self.PrevDevice = self.Device
                self.Device = foundDev
                
            else:
                serialComm.Indicator = "No Device Connected"
                self.PrevDevice = self.Device
                self.Device = foundDev
        
        #print('self.Device = ', self.Device)
        #print('self.PrevDevice = ', self.PrevDevice)
        
    def initDeviceStatus(self):
        foundDev = self.findPacemaker()
        if(foundDev != None):
            serialComm.Indicator = "New Device Connected"
        else:
            serialComm.Indicator = "No Device Connected"

    #Read 1 byte of data
    def readData(self):
        if(self.Device == self.findPacemaker()):
            size = ser.inWaiting()
            hexstr = 0
            if size >0:
                readBytes = ser.read(size)
                y_data = unpack('d', readBytes)
                y_data = y_data[0]
                
        return y_data

    def writeParameters(self, mode):
        if(self.Device == self.findPacemaker()):
            modeStr = str(mode)
            modeByte = str.encode(modeStr)

            #Set Syncronoization byte and write byte
            Sync = str.encode("\x16")
            Write = str.encode("\x55")

            #Read parameters and set byte data
            bytePack = []
            f = open("ParameterData.txt","r")
            for i in range(0,17):
                param = f.readline()
                bytePack.append(param)

            strByte = b''
            for i in bytePack:
                strByte = strByte + i.to_bytes(2, 'little')
            finalByte = Sync + Write + modeByte + strByte
            ser.write(finalByte)

    
    def getPacemakerCount(self):
        return len(self.Devices)
    
    def getDevices(self):
        return self.Devices
    
    def getPrevDevice(self):
        return self.prevInterogated
    
    def getDevice(self):
        return self.Device

            
            
        
