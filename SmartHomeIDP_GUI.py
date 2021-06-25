import tkinter as Tkinter
import tkinter.messagebox as tkMessageBox

import picamera  
import time  
import Adafruit_DHT  
import RPi.GPIO as GPIO  
from RPLCD.i2c import CharLCD  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT) 
GPIO.setup(21,GPIO.OUT)

lcd=CharLCD("PCF8574",0x27)  
camera=picamera.PiCamera()  
camera.resolution=(2592,1944)  
intrusion_control=0  
timer=0  
dht_type=11
bcm_pin=23

def bellRing(on):
    if on:
        while True:  
            pitch=1000  
            duration=0.1
            period=1.0/pitch  
            delay=period/2  
            cycles=int(duration*pitch)  
            
            for i in range(cycles):  
                GPIO.output(25,True)  
                time.sleep(delay)  
                GPIO.output(25,False)  
                time.sleep(delay)
                
        time.sleep(0.5)
    else:
        GPIO.cleanup()

def showTempAndHum():
    lcd.clear()    
    humidity,temperature=Adafruit_DHT.read_retry(dht_type,bcm_pin)  
    humid=round(humidity,1)  
    temp=round(temperature,1)  
    print(humid,temp)  
    lcd.write_string('TEMP')  
    lcd.write_string(str(temp))  
    lcd.write_string('C')  
    lcd.crlf()  
    lcd.write_string('HUMID')  
    lcd.write_string(str(humid))  
    lcd.write_string('%')

def emergencyLight(on):
    if on:
        while True:  
            GPIO.output(16,True)   
            time.sleep(0.1)  
            GPIO.output(16,False)  
            time.sleep(0.1)  
            GPIO.output(20,True)  
            time.sleep(0.1)  
            GPIO.output(20,False)  
            time.sleep(0.1)  
            GPIO.output(21,True)  
            time.sleep(0.1)  
            GPIO.output(21,False)  
            time.sleep(0.1)
    else:
        GPIO.cleanup()
  
def camera():
    camera.capture("photo.jpg")  
    tkMessageBox.showinfo( "Camera", "Phote is saved!")

top = Tkinter.Tk()
top.title("Smart Home")

Bell = Tkinter.Button(top, text ="Bell ring", command = bellRing(True))
BellOff = Tkinter.Button(top, text ="Bell off", command = bellRing(False))
Temperature = Tkinter.Button(top, text ="Show Temp", command = showTempAndHum())
LightOn = Tkinter.Button(top, text ="Light Blink", command = emergencyLight(True))
LightOff = Tkinter.Button(top, text ="Light Off", command = emergencyLight(False))
Camera  = Tkinter.Button(top, text ="Take Picture", command = camera())

Bell.pack()
BellOff.pack()
Temperature.pack()
LightOn.pack()
LightOff.pack()
Camera.pack()
top.mainloop()