import random, pyautogui, sys
import win32gui, win32api, win32con
import time
import ctypes
from win32gui import *
from ByteBeat import *

lastMousePos = pyautogui.position()

while lastMousePos == pyautogui.position():
    pass


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
hdc = win32gui.GetDC(0)
dx = dy = 1
size = 2.9
speed = 0.15
color = -100
angle = 90
byte1 = "(-t*4-1)*(t*4%512 < 190)"
byte3 = "(-t*4-1)*(t*3%502 < 190)"


messageBox = 0 #ctypes.windll.user32.MessageBoxW(0, u"This program contains flashing lights.\n Continue?", u"Epilepsy warning", 0x04 | 0x30) # warning (optional ofc)

if messageBox == 7:
    sys.exit(0)

beat = ByteBeat.GenerateBuffer(byte1 and byte3, 30, 4000)
ByteBeat.PlayFromBuffer(beat, 30, 4000, False)

screen_size = win32gui.GetWindowRect(win32gui.GetDesktopWindow())

left = screen_size[0]
top = screen_size[1]
right = screen_size[2]
bottom = screen_size[3]


lpppoint = ((left - 50, top + 50), (right - 50, top - 50), (left + 50, bottom + 50))


while True:

    hdc = win32gui.GetDC(0)
    mhdc = CreateCompatibleDC(hdc)
    hbit = CreateCompatibleBitmap(hdc, sh, sw)
    holdbit = SelectObject(mhdc, hbit)

    PlgBlt(
        hdc,
        lpppoint,
        hdc,
        left - 20,
        top - 20,
        (right - left) + 40,
        (bottom - top) + 40,
        None,
        0,
        0,
    )
    
    win32gui.InvertRect(hdc, (0, 0, sw, sh))
    
    hdc = win32gui.GetDC(0)
    x = random.randint(0, sw)
    win32gui.BitBlt(hdc, x, 1, 10, sh, hdc, x, 0, win32con.SRCCOPY)
    win32gui.ReleaseDC(0, hdc)
