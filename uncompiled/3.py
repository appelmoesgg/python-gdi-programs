import random, pyautogui, sys
import win32gui, win32con
import ctypes
from win32gui import *

###################################BYTEBEAT IMPORT START##############################################
################################## [Copyright to Itzsten on Github] ####################################

import ctypes
from ctypes import byref, create_string_buffer, c_byte, POINTER, sizeof
from win32api import Sleep
from functools import partial

class Infix(object):
	def __init__(self, func): self.func = func
	def __or__(self, other): return self.func(other)
	def __ror__(self, other): return Infix(partial(self.func, other))
	def __call__(self, v1, v2): return self.func(v1, v2)
LPSTR,BYTE,WORD,UINT,DWORD,HANDLE=ctypes.c_char_p,ctypes.c_byte,ctypes.c_ushort,ctypes.c_uint,ctypes.c_ulong,ctypes.c_void_p
HWAVEOUT = HANDLE
LPHWAVEOUT = POINTER(HWAVEOUT)
winmm = ctypes.windll.Winmm
waveOutOpen,waveOutPrepareHeader,waveOutWrite,waveOutUnprepareHeader,waveOutClose=winmm.waveOutOpen,winmm.waveOutPrepareHeader,winmm.waveOutWrite,winmm.waveOutUnprepareHeader,winmm.waveOutClose
WAVE_FORMAT_PCM,WAVE_MAPPER,CALLBACK_NULL=1,-1,0

class WAVEFORMATEX(ctypes.Structure): 
		_fields_ = [ 
			("wFormatTag", WORD), 
			("nChannels", WORD), 
			("nSamplesPerSec", DWORD), 
			("nAvgBytesPerSec", DWORD), 
			("nBlockAlign", WORD), 
			("wBitsPerSample", WORD), 
			("cbSize", WORD) 
		] 
LPWAVEFORMATEX = POINTER(WAVEFORMATEX) 
class WAVEHDR(ctypes.Structure): 
	pass 
LPWAVEHDR = POINTER(WAVEHDR) 
WAVEHDR._fields_ = [ 
	("lpData", LPSTR), 
	("dwBufferLength", DWORD), 
	("dwBytesRecorded", DWORD), 
	("dwUser", DWORD), 
	("dwFlags", DWORD), 
	("dwLoops", DWORD), 
	("lpNext", LPWAVEHDR), 
	("reserved", DWORD) 
]
LPWAVEHDR = POINTER(WAVEHDR)

# fixes js only stuff
division_key_fix=Infix(lambda x,y: x/y if y else 0)
operand_key_fix=Infix(lambda x,y: int(x)|int(y))
charcodeat_key_fix=Infix(lambda s,y: ord(s[y]))
operand_gtgt_key_fix=Infix(lambda x,y: int(x)>>int(y))
operand_ltlt_key_fix=Infix(lambda x, y: int(x)<<int(y))
operand_and_key_fix=Infix(lambda x, y: int(x)&int(y))

class ByteBeat:
	def GenerateBuffer(EQUATION, SECONDS_PLAYING, AMOUNT_KILOHERTZ=8000):
		'''
		> GenerateBuffer function
		- Generates buffering data playable via the PlayFromBuffer function
		@ EQUATION argument: Mathematical ByteBeat input eg. 't%0.86*t'
		@ EQUATION type: str
		@ SECONDS_PLAYING argument: The length of the ByteBeat, in seconds
		@ SECONDS_PLAYING type: int
		@ AMOUNT_KILOHERTZ argument: The amount of kilohertz (kHz) the ByteBeat will use.
		@ AMOUNT_KILOHERTZ type: int
		'''
		EQUATION = EQUATION.replace('^','**').replace('random()','__import__("random").random()').replace('|','|operand_key_fix|').replace('/','|division_key_fix|').replace('?',' if ').replace(':',' else ').replace('.charCodeAt',' |charcodeat_key_fix| ').replace('>>',' |operand_gtgt_key_fix| ').replace('<<',' |operand_ltlt_key_fix| ').replace('&', ' |operand_and_key_fix| ')
		hWaveOut = HWAVEOUT(0)
		wfx = WAVEFORMATEX(WAVE_FORMAT_PCM, 1, AMOUNT_KILOHERTZ, AMOUNT_KILOHERTZ, 1, 8,0)
		waveOutOpen(byref(hWaveOut), WAVE_MAPPER, LPWAVEFORMATEX(wfx), 0, 0, CALLBACK_NULL)
		buffer = create_string_buffer(int(AMOUNT_KILOHERTZ) * SECONDS_PLAYING)
		for t in range(0, int(AMOUNT_KILOHERTZ) * SECONDS_PLAYING):buffer.value += c_byte(int(eval(EQUATION)))
		return buffer.raw

	def Play(EQUATION, SECONDS_PLAYING, AMOUNT_KILOHERTZ, ASYNC_SLEEP = False):
		'''
		> Play function
		- Generates buffering data and plays the result when it finished.
		@ EQUATION argument: Mathematical ByteBeat input eg. 't%0.86*t'
		@ EQUATION type: str
		@ SECONDS_PLAYING argument: The length of the ByteBeat, in seconds
		@ SECONDS_PLAYING type: int
		@ AMOUNT_KILOHERTZ argument: The amount of kilohertz (kHz) the ByteBeat will use.
		@ AMOUNT_KILOHERTZ type: int
		@ ASYNC_SLEEP argument: Wait until the sound playing has finished or not.
		@ ASYNC_SLEEP type: bool
		'''
		EQUATION = EQUATION.replace('^','**').replace('random()','__import__("random").random()').replace('|','|operand_key_fix|').replace('/','|division_key_fix|').replace('?',' if ').replace(':',' else ').replace('.charCodeAt',' |charcodeat_key_fix| ').replace('>>',' |operand_gtgt_key_fix| ').replace('<<',' |operand_ltlt_key_fix| ').replace('&', ' |operand_and_key_fix| ')
		hWaveOut = HWAVEOUT(0)
		wfx = WAVEFORMATEX(WAVE_FORMAT_PCM, 1, AMOUNT_KILOHERTZ, AMOUNT_KILOHERTZ, 1, 8,0)
		winmm.waveOutOpen.argtypes = (LPHWAVEOUT, UINT, LPWAVEFORMATEX, DWORD, DWORD, DWORD) 
		waveOutOpen(byref(hWaveOut), WAVE_MAPPER, LPWAVEFORMATEX(wfx), 0, 0, CALLBACK_NULL)
		buffer = create_string_buffer(int(AMOUNT_KILOHERTZ) * SECONDS_PLAYING)
		for t in range(0, int(AMOUNT_KILOHERTZ) * SECONDS_PLAYING):buffer.value += c_byte(int(eval(EQUATION)))
		buffer = buffer.raw
		wHeader = WAVEHDR(buffer, len(buffer), 0, 0, 0, 0)
		waveOutPrepareHeader(hWaveOut, byref(wHeader), sizeof(WAVEHDR))
		waveOutWrite(hWaveOut, byref(wHeader), sizeof(WAVEHDR))
		waveOutUnprepareHeader(hWaveOut, byref(wHeader), sizeof(WAVEHDR))
		waveOutClose(hWaveOut)
		if ASYNC_SLEEP: Sleep(SECONDS_PLAYING*1000)
		return True
	def PlayFromBuffer(buffer, SECONDS_PLAYING, AMOUNT_KILOHERTZ, ASYNC_SLEEP=False):
		'''
		> PlayFromBuffer function
		- Plays buffering data generatable using the GenerateBuffer function
		@ buffer argument: String buffering data
		@ buffer type: str
		@ SECONDS_PLAYING argument: The length of the ByteBeat, in seconds
		@ SECONDS_PLAYING type: int
		@ AMOUNT_KILOHERTZ argument: The amount of kilohertz (kHz) the ByteBeat will use
		@ AMOUNT_KILOHERTZ type: int
		@ ASYNC_SLEEP argument: Wait until the sound playing has finished or not
		@ ASYNC_SLEEP type: bool
		'''
		hWaveOut = HWAVEOUT(0)
		wfx = WAVEFORMATEX(WAVE_FORMAT_PCM, 1, AMOUNT_KILOHERTZ, AMOUNT_KILOHERTZ, 1, 8,0)
		waveOutOpen(byref(hWaveOut), WAVE_MAPPER, LPWAVEFORMATEX(wfx), 0, 0, CALLBACK_NULL)
		wHeader = WAVEHDR(buffer, len(buffer), 0, 0, 0, 0)
		waveOutPrepareHeader(hWaveOut, byref(wHeader), sizeof(WAVEHDR))
		waveOutWrite(hWaveOut, byref(wHeader), sizeof(WAVEHDR))
		waveOutUnprepareHeader(hWaveOut, byref(wHeader), sizeof(WAVEHDR))
		waveOutClose(hWaveOut)
		if ASYNC_SLEEP: Sleep(SECONDS_PLAYING*1000)
		return True

###################################BYTEBEAT END##############################################

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


messageBox = 0 #ctypes.windll.user32.MessageBoxW(0, u"This program contains flashing lights.\n Continue?", u"Epilepsy warning", 0x04 | 0x30) # WARNING|optional ofc :)

if messageBox == 7:
    sys.exit(0)
    
lastMousePos = pyautogui.position()

while lastMousePos == pyautogui.position():
    pass

beat = ByteBeat.GenerateBuffer(byte1 and byte3, 30, 4000)
ByteBeat.PlayFromBuffer(beat, 30, 4000, False)

screen_size = win32gui.GetWindowRect(win32gui.GetDesktopWindow())

left = screen_size[0]
top = screen_size[1]
right = screen_size[2]
bottom = screen_size[3]


lpppoint = ((left - 50, top + 50), (right - 50, top - 50), (left + 50, bottom + 50))


while True:
    if keyboard.is_pressed("ctrl+shift+i"): #stop function
        break

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
    
