import machine 
import network
import time
import urequests

def googleconnect():
    try:
        s = urequests.get("https://www.google.com")
        print(s.status_code)
        return True
    except:
        print("Connection to Google failed.")
        return False
def connect(ssid, password):
    newmac = bytearray([0x32, 0xAE, 0xA4, 0x07, 0x0D, 0x66])

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting...")
        i = 0
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            time.sleep(1)
            i+=1
            if (i > 10):
                print("Wifi Connection Could Not Be Established")
                wlan.active(False)
                return False
    print("Connected to Wifi.")
    print("IP Address:", wlan.ifconfig()[0])
    if googleconnect():
        return True
    return False
