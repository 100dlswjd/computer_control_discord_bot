import os
import sys
import ctypes
import time
import random

DD_KEY_PRESS = 1 #키다운
DD_KEY_RELEASE = 2 #키업

VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'f1':0x70,
           'f2':0x71,
           'f3':0x72,
           'f4':0x73,
           'f5':0x74,
           'f6':0x75,
           'f7':0x76,
           'f8':0x77,
           'f9':0x78,
           'f10':0x79,
           'f11':0x7A,
           'f12':0x7B,
           'f13':0x7C,
           'f14':0x7D,
           'f15':0x7E,
           'f16':0x7F,
           'f17':0x80,
           'f18':0x81,
           'f19':0x82,
           'f20':0x83,
           'f21':0x84,
           'f22':0x85,
           'f23':0x86,
           'f24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# dd64 = resource_path("src/dll/DD64.dll")
dd64 = resource_path("dll/DD64.dll")
mydll = ctypes.windll.LoadLibrary(dd64)

DD_key = mydll["DD_key"]
DD_key.argtypes = (ctypes.c_int32, ctypes.c_int32)
DD_key.restype = ctypes.c_int32

DD_todc = mydll["DD_todc"]
DD_todc.argtypes = (ctypes.c_int32,)
DD_todc.restype = ctypes.c_int32

def press(key : str):
    key = key.lower()
    key_code = VK_CODE[key]
    code = DD_todc(key_code)
    DD_key(code, DD_KEY_PRESS)
    time.sleep(random.uniform(0.08,0.1))
    DD_key(code, DD_KEY_RELEASE)

def pressAndHold(key : str):
    key = key.lower()
    key_code = VK_CODE[key]
    code = DD_todc(key_code)
    DD_key(code, DD_KEY_PRESS)

def release(key : str):
    key = key.lower()
    key_code = VK_CODE[key]
    code = DD_todc(key_code)
    DD_key(code, DD_KEY_RELEASE)
