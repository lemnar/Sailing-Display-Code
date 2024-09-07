import connecttowifi
import espapidata as api
import displayitem

def main():
    displayitem.display.fill_rectangle(0, 0, 240, 320, 0xcf18)
    displayitem.text(displayitem.display, "Connecting To Wifi...",0, 50, background=0)
    try: 
        connecttowifi.connect("wifi1", "passwordtowifi1")
        data = api.do()
        displayitem.main(data)
    except:
        try: 
            connecttowifi.connect("wifi2", "passwordtowifi2")
            data = api.do()
            displayitem.main(data)
        except:
            
            try:
                connecttowifi.connect("wifi3", "passwordtowifi3")
                data = api.do()
                displayitem.main(data)
            except: 
                displayitem.display.fill_rectangle(0, 0, 240, 320, 0xcf18)
                displayitem.text(displayitem.display, "Wifi Connection Failed", background=0)
