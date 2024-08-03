#!/usr/bin/env python

''' Autorem kodu jest Wiesław Sidor @siehu, pomysłodawca Tomasz Markiewicz @MarkielPL.
    Skrypt ma na celu pobieranie danych z czujnika DHT_11 i przesyłanie ich do wskazanych diod,
    przy wykorzystaniu biblioteki Adafruit_DHT.

    Program jest napisany zgodnie z Licencja MIT. Autorzy wyrażają zgodę na nieograniczone prawo
    do używania, kopiowania, modyfikowania i rozpowszechniania bez możliwości sprzedaży oryginalnego
    lub zmodyfikowanego programu w postaci binarnej lub źródłowej. Wymagamy, by we wszystkich
    wersjach zachowano warunki licencyjne i informacje o autorze.'''

import time
import sys
import Adafruit_DHT
from gpiozero import LED
from threading import Thread

blue = LED(20)
green = LED(21)
red = LED(26)

# globalne zmienne dla obu watkow
humidity = 0
temperature = 0

red_temp_on = False

def blink_humidity():
    # print("watek start")
    b_on = False  # stan diody niebieskiej

    def mrugnij(hz):  # fun odwraca czestotliwosc w czas spania
        #print(f'mrugam {hz} Hz')
        time.sleep(1/hz)

    while True:
        #print(f'test wilgotnosci:{humidity}')
        if humidity < 45:
            # print("niska wilgotnosc (<45)")
            if b_on:
                # print("dioda niebieska on, daje off")
                blue.off()
                #red.off()
                b_on = False
            else:
                # print("dioda niebieska off, daje on")
                blue.on()
                #red.off()
                b_on = True

            time.sleep(0.25)
            blue.off()
            b_on = False
            mrugnij(0.5)  # zmiana stanu co 1 Hz
        elif 45 <= humidity <= 60:
            # print("srednia wilgotnosc 45-60")
            if b_on:
                # print("dioda niebieska on, daje off")
                blue.off()
                #red.off()
                b_on = False
            else:
                # print("dioda niebieska off, daje on")
                blue.on()
                #red.off()
                b_on = True
            time.sleep(0.25)
            blue.off()
            b_on = False
            mrugnij(1)  # zmiana stanu co 0.5 Hz
        else:
            # print("duza wilgotnosc >60")
            if b_on:
                # print("dioda niebieska on, daje off")
                blue.off()
                red.on()
                b_on = False
            else:
                # print("dioda niebieska off, daje on")
                blue.on()
                red.off()
                b_on = True
            mrugnij(2)  # zmiana stanu co 2 Hz
        
        if red_temp_on:
            red.on()

def handle_sensor():
    global humidity
    global temperature

    while (True):
        # Creates two random values for sending data
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 14)
        #humidity = 45
        #temperature = 22

        print(f'temp: {temperature}, hum:{humidity}')

        # Handle temperature LED status
        if temperature > 25:
            #print("zapalam czerwona")
            green.off()
            red.on()
            red_temp_on = True
        else:
            #print("zapalam zielona")
            green.on()
            red.off()
            red_temp_on = False
        time.sleep(60)


if __name__ == '__main__':
    t1 = Thread(target=blink_humidity)
    t2 = Thread(target=handle_sensor)
    t1.start()
    t2.start()
    t1.join()
    #t2.join()
