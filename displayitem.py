import machine
import ili9341
import framebuf
import time

# Define the pins for SPI communication
spi = machine.SPI(
    1,  # SPI bus
    baudrate=20000000,  # 10 MHz (you may need to adjust this based on your display)
    sck=machine.Pin(18),  # SCK pin
    mosi=machine.Pin(23),  # MOSI pin
)

def text(display, text, x=0, y=0, w=240,h=40, pad_top = 10, pad_left=20,color=0xffff, background=0x0000):
    buffer = bytearray(w * h * 2)
    fb = framebuf.FrameBuffer(buffer, w, h, framebuf.RGB565)
    fb.fill(background)
    fb.text(text, pad_left, pad_top, color)
    display.blit_buffer(buffer, x,y,w, h)
    
    # for line in text.split('\n'):
    #     fb.text(line, 10, 100, color)
    #     display.blit_buffer(buffer, 10, 0, 200, 20)
    #     y += 8
    #     if y >= display.height:
    #         break

def drawUnhappyFace(display):
    display.fill_rectangle(x=0,y=0,width=240,height=320,color=0x6d9c)
    text(display, "Nikky's Sail Indicator TM", 0, 0, pad_top=6, h=20, pad_left=20,background=0xffff, color=0)
    display.fill_rectangle(45, 80, 150, 150, 0x0000)
    display.fill_rectangle(50, 85, 140, 140, 0xe7e0)
    display.fill_rectangle(90, 115, 10, 10, 0x0000)
    display.fill_rectangle(140, 115, 10, 10, 0x0000)
    display.fill_rectangle(70, 180, 100, 5, 0x0000)
    text(display, "Bad Conditions for Sailing :(", 0,260,h=60,pad_top=20,pad_left=5,background=0)

def drawSailboat(display, times = None, w = 0, t = 0, c = 0, g = 0, p = 0):
    if times is None: 
        drawUnhappyFace(display)
        return
    display.fill_rectangle(x=0,y=0,width=240,height=320,color=0x6d9c)
    text(display, "Nikky's Sail Indicator TM", 0, 0, pad_top=6, h=20, pad_left=20,background=0xffff, color=0)
    # boat base
    display.fill_rectangle(0,200,240,120, 0x0000ff)
    display.fill_rectangle(82,176,106,35, 0x8410)
    display.fill_rectangle(53,176,82-53,16, 0x8410)
    display.fill_rectangle(64,176+16,82-64,11, 0x8410)
    #mast
    display.fill_rectangle(89,90,8,176-90,0xc658)
    # main sail
    display.fill_rectangle(97,90,17,24,0xffff)
    display.fill_rectangle(97,90+24,30,24,0xffff)
    display.fill_rectangle(97,90+24+24,43,24,0xffff)
    # jib sail
    display.fill_rectangle(89-11, 106, 11, 66, 0xffff)
    display.fill_rectangle(89-11-10, 106+66-40, 10, 40, 0xffff)
    display.fill_rectangle(89-11-10-10, 106+66-21, 10, 21, 0xffff)
    
    text(display, "Great Conditions for Sailing!", 0,256,h=16,pad_top=4,pad_left=5,background=0)
    text(display,"time: {}".format(times), 0, 272, w=120, h=16, pad_top=4,pad_left=2,background=0)
    text(display,"wind: {}".format(w), 120, 272, w=120, h=16, pad_top=4,pad_left=2,background=0)
    text(display,"temp: {}".format(t), 0, 288, w=120, h=16, pad_top=4,pad_left=2,background=0)
    text(display,"clouds: {}".format(c), 120, 288, w=120, h=16, pad_top=4,pad_left=2,background=0)
    text(display,"gust: {}".format(g), 0, 304, w=120, h=16, pad_top=4,pad_left=2,background=0)
    text(display,"precip: {}".format(p), 120, 304, w=120, h=16, pad_top=4,pad_left=2,background=0)

# Create an ST7735 display object
display = ili9341.ILI9341(spi, width=240, height=320, cs=machine.Pin(4), dc=machine.Pin(19), rst=machine.Pin(22))
def main(data):
    if data:
        try:
            drawSailboat(display, data[0].hour, data[0].wind, data[0].temp, data[0].cloud, data[0].gust, data[0].precip)
        except:
            drawUnhappyFace(display)
    else: 
        drawUnhappyFace(display)
if __name__ == "__main__" :
    main()