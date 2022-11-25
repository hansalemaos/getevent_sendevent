import os
import struct
import subprocess
import tempfile
from time import sleep

import psutil
import regex
import numpy as np
import pandas as pd
import keyboard as keyboard__
from flatten_everything import flatten_everything
from flexible_partial import FlexiblePartial
from more_itertools import chunked, windowed
from touchtouch import touch
from PrettyColorPrinter import add_printer

add_printer(True)
int_array = np.frompyfunc(int, 2, 1)

keycodeslinux = {
    "INPUT_PROP_POINTER": 0x00,
    "INPUT_PROP_DIRECT": 0x01,
    "INPUT_PROP_BUTTONPAD": 0x02,
    "INPUT_PROP_SEMI_MT": 0x03,
    "INPUT_PROP_TOPBUTTONPAD": 0x04,
    "INPUT_PROP_POINTING_STICK": 0x05,
    "INPUT_PROP_ACCELEROMETER": 0x06,
    "INPUT_PROP_MAX": 0x1F,
    "INPUT_PROP_CNT": 0x1F + 1,
    "EV_SYN": 0x00,
    "EV_KEY": 0x01,
    "EV_REL": 0x02,
    "EV_ABS": 0x03,
    "EV_MSC": 0x04,
    "EV_SW": 0x05,
    "EV_LED": 0x11,
    "EV_SND": 0x12,
    "EV_REP": 0x14,
    "EV_FF": 0x15,
    "EV_PWR": 0x16,
    "EV_FF_STATUS": 0x17,
    "EV_MAX": 0x1F,
    "EV_CNT": (0x1F + 1),
    "SYN_REPORT": 0,
    "SYN_CONFIG": 1,
    "SYN_MT_REPORT": 2,
    "SYN_DROPPED": 3,
    "SYN_MAX": 0xF,
    "SYN_CNT": (0xF + 1),
    "KEY_RESERVED": 0,
    "KEY_ESC": 1,
    "KEY_1": 2,
    "KEY_2": 3,
    "KEY_3": 4,
    "KEY_4": 5,
    "KEY_5": 6,
    "KEY_6": 7,
    "KEY_7": 8,
    "KEY_8": 9,
    "KEY_9": 10,
    "KEY_0": 11,
    "KEY_MINUS": 12,
    "KEY_EQUAL": 13,
    "KEY_BACKSPACE": 14,
    "KEY_TAB": 15,
    "KEY_Q": 16,
    "KEY_W": 17,
    "KEY_E": 18,
    "KEY_R": 19,
    "KEY_T": 20,
    "KEY_Y": 21,
    "KEY_U": 22,
    "KEY_I": 23,
    "KEY_O": 24,
    "KEY_P": 25,
    "KEY_LEFTBRACE": 26,
    "KEY_RIGHTBRACE": 27,
    "KEY_ENTER": 28,
    "KEY_LEFTCTRL": 29,
    "KEY_A": 30,
    "KEY_S": 31,
    "KEY_D": 32,
    "KEY_F": 33,
    "KEY_G": 34,
    "KEY_H": 35,
    "KEY_J": 36,
    "KEY_K": 37,
    "KEY_L": 38,
    "KEY_SEMICOLON": 39,
    "KEY_APOSTROPHE": 40,
    "KEY_GRAVE": 41,
    "KEY_LEFTSHIFT": 42,
    "KEY_BACKSLASH": 43,
    "KEY_Z": 44,
    "KEY_X": 45,
    "KEY_C": 46,
    "KEY_V": 47,
    "KEY_B": 48,
    "KEY_N": 49,
    "KEY_M": 50,
    "KEY_COMMA": 51,
    "KEY_DOT": 52,
    "KEY_SLASH": 53,
    "KEY_RIGHTSHIFT": 54,
    "KEY_KPASTERISK": 55,
    "KEY_LEFTALT": 56,
    "KEY_SPACE": 57,
    "KEY_CAPSLOCK": 58,
    "KEY_F1": 59,
    "KEY_F2": 60,
    "KEY_F3": 61,
    "KEY_F4": 62,
    "KEY_F5": 63,
    "KEY_F6": 64,
    "KEY_F7": 65,
    "KEY_F8": 66,
    "KEY_F9": 67,
    "KEY_F10": 68,
    "KEY_NUMLOCK": 69,
    "KEY_SCROLLLOCK": 70,
    "KEY_KP7": 71,
    "KEY_KP8": 72,
    "KEY_KP9": 73,
    "KEY_KPMINUS": 74,
    "KEY_KP4": 75,
    "KEY_KP5": 76,
    "KEY_KP6": 77,
    "KEY_KPPLUS": 78,
    "KEY_KP1": 79,
    "KEY_KP2": 80,
    "KEY_KP3": 81,
    "KEY_KP0": 82,
    "KEY_KPDOT": 83,
    "KEY_ZENKAKUHANKAKU": 85,
    "KEY_102ND": 86,
    "KEY_F11": 87,
    "KEY_F12": 88,
    "KEY_RO": 89,
    "KEY_KATAKANA": 90,
    "KEY_HIRAGANA": 91,
    "KEY_HENKAN": 92,
    "KEY_KATAKANAHIRAGANA": 93,
    "KEY_MUHENKAN": 94,
    "KEY_KPJPCOMMA": 95,
    "KEY_KPENTER": 96,
    "KEY_RIGHTCTRL": 97,
    "KEY_KPSLASH": 98,
    "KEY_SYSRQ": 99,
    "KEY_RIGHTALT": 100,
    "KEY_LINEFEED": 101,
    "KEY_HOME": 102,
    "KEY_UP": 103,
    "KEY_PAGEUP": 104,
    "KEY_LEFT": 105,
    "KEY_RIGHT": 106,
    "KEY_END": 107,
    "KEY_DOWN": 108,
    "KEY_PAGEDOWN": 109,
    "KEY_INSERT": 110,
    "KEY_DELETE": 111,
    "KEY_MACRO": 112,
    "KEY_MUTE": 113,
    "KEY_VOLUMEDOWN": 114,
    "KEY_VOLUMEUP": 115,
    "KEY_POWER": 116,
    "KEY_KPEQUAL": 117,
    "KEY_KPPLUSMINUS": 118,
    "KEY_PAUSE": 119,
    "KEY_SCALE": 120,
    "KEY_KPCOMMA": 121,
    "KEY_HANGEUL": 122,
    "KEY_HANGUEL": 122,
    "KEY_HANJA": 123,
    "KEY_YEN": 124,
    "KEY_LEFTMETA": 125,
    "KEY_RIGHTMETA": 126,
    "KEY_COMPOSE": 127,
    "KEY_STOP": 128,
    "KEY_AGAIN": 129,
    "KEY_PROPS": 130,
    "KEY_UNDO": 131,
    "KEY_FRONT": 132,
    "KEY_COPY": 133,
    "KEY_OPEN": 134,
    "KEY_PASTE": 135,
    "KEY_FIND": 136,
    "KEY_CUT": 137,
    "KEY_HELP": 138,
    "KEY_MENU": 139,
    "KEY_CALC": 140,
    "KEY_SETUP": 141,
    "KEY_SLEEP": 142,
    "KEY_WAKEUP": 143,
    "KEY_FILE": 144,
    "KEY_SENDFILE": 145,
    "KEY_DELETEFILE": 146,
    "KEY_XFER": 147,
    "KEY_PROG1": 148,
    "KEY_PROG2": 149,
    "KEY_WWW": 150,
    "KEY_MSDOS": 151,
    "KEY_COFFEE": 152,
    "KEY_SCREENLOCK": 152,
    "KEY_ROTATE_DISPLAY": 153,
    "KEY_DIRECTION": 153,
    "KEY_CYCLEWINDOWS": 154,
    "KEY_MAIL": 155,
    "KEY_BOOKMARKS": 156,
    "KEY_COMPUTER": 157,
    "KEY_BACK": 158,
    "KEY_FORWARD": 159,
    "KEY_CLOSECD": 160,
    "KEY_EJECTCD": 161,
    "KEY_EJECTCLOSECD": 162,
    "KEY_NEXTSONG": 163,
    "KEY_PLAYPAUSE": 164,
    "KEY_PREVIOUSSONG": 165,
    "KEY_STOPCD": 166,
    "KEY_RECORD": 167,
    "KEY_REWIND": 168,
    "KEY_PHONE": 169,
    "KEY_ISO": 170,
    "KEY_CONFIG": 171,
    "KEY_HOMEPAGE": 172,
    "KEY_REFRESH": 173,
    "KEY_EXIT": 174,
    "KEY_MOVE": 175,
    "KEY_EDIT": 176,
    "KEY_SCROLLUP": 177,
    "KEY_SCROLLDOWN": 178,
    "KEY_KPLEFTPAREN": 179,
    "KEY_KPRIGHTPAREN": 180,
    "KEY_NEW": 181,
    "KEY_REDO": 182,
    "KEY_F13": 183,
    "KEY_F14": 184,
    "KEY_F15": 185,
    "KEY_F16": 186,
    "KEY_F17": 187,
    "KEY_F18": 188,
    "KEY_F19": 189,
    "KEY_F20": 190,
    "KEY_F21": 191,
    "KEY_F22": 192,
    "KEY_F23": 193,
    "KEY_F24": 194,
    "KEY_PLAYCD": 200,
    "KEY_PAUSECD": 201,
    "KEY_PROG3": 202,
    "KEY_PROG4": 203,
    "KEY_ALL_APPLICATIONS": 204,
    "KEY_DASHBOARD": 204,
    "KEY_SUSPEND": 205,
    "KEY_CLOSE": 206,
    "KEY_PLAY": 207,
    "KEY_FASTFORWARD": 208,
    "KEY_BASSBOOST": 209,
    "KEY_PRINT": 210,
    "KEY_HP": 211,
    "KEY_CAMERA": 212,
    "KEY_SOUND": 213,
    "KEY_QUESTION": 214,
    "KEY_EMAIL": 215,
    "KEY_CHAT": 216,
    "KEY_SEARCH": 217,
    "KEY_CONNECT": 218,
    "KEY_FINANCE": 219,
    "KEY_SPORT": 220,
    "KEY_SHOP": 221,
    "KEY_ALTERASE": 222,
    "KEY_CANCEL": 223,
    "KEY_BRIGHTNESSDOWN": 224,
    "KEY_BRIGHTNESSUP": 225,
    "KEY_MEDIA": 226,
    "KEY_SWITCHVIDEOMODE": 227,
    "KEY_KBDILLUMTOGGLE": 228,
    "KEY_KBDILLUMDOWN": 229,
    "KEY_KBDILLUMUP": 230,
    "KEY_SEND": 231,
    "KEY_REPLY": 232,
    "KEY_FORWARDMAIL": 233,
    "KEY_SAVE": 234,
    "KEY_DOCUMENTS": 235,
    "KEY_BATTERY": 236,
    "KEY_BLUETOOTH": 237,
    "KEY_WLAN": 238,
    "KEY_UWB": 239,
    "KEY_UNKNOWN": 240,
    "KEY_VIDEO_NEXT": 241,
    "KEY_VIDEO_PREV": 242,
    "KEY_BRIGHTNESS_CYCLE": 243,
    "KEY_BRIGHTNESS_AUTO": 244,
    "KEY_BRIGHTNESS_ZERO": 244,
    "KEY_DISPLAY_OFF": 245,
    "KEY_WWAN": 246,
    "KEY_WIMAX": 246,
    "KEY_RFKILL": 247,
    "KEY_MICMUTE": 248,
    "BTN_MISC": 0x100,
    "BTN_0": 0x100,
    "BTN_1": 0x101,
    "BTN_2": 0x102,
    "BTN_3": 0x103,
    "BTN_4": 0x104,
    "BTN_5": 0x105,
    "BTN_6": 0x106,
    "BTN_7": 0x107,
    "BTN_8": 0x108,
    "BTN_9": 0x109,
    "BTN_MOUSE": 0x110,
    "BTN_LEFT": 0x110,
    "BTN_RIGHT": 0x111,
    "BTN_MIDDLE": 0x112,
    "BTN_SIDE": 0x113,
    "BTN_EXTRA": 0x114,
    "BTN_FORWARD": 0x115,
    "BTN_BACK": 0x116,
    "BTN_TASK": 0x117,
    "BTN_JOYSTICK": 0x120,
    "BTN_TRIGGER": 0x120,
    "BTN_THUMB": 0x121,
    "BTN_THUMB2": 0x122,
    "BTN_TOP": 0x123,
    "BTN_TOP2": 0x124,
    "BTN_PINKIE": 0x125,
    "BTN_BASE": 0x126,
    "BTN_BASE2": 0x127,
    "BTN_BASE3": 0x128,
    "BTN_BASE4": 0x129,
    "BTN_BASE5": 0x12A,
    "BTN_BASE6": 0x12B,
    "BTN_DEAD": 0x12F,
    "BTN_GAMEPAD": 0x130,
    "BTN_SOUTH": 0x130,
    "BTN_A": 0x130,
    "BTN_EAST": 0x131,
    "BTN_B": 0x131,
    "BTN_C": 0x132,
    "BTN_NORTH": 0x133,
    "BTN_X": 0x133,
    "BTN_WEST": 0x134,
    "BTN_Y": 0x134,
    "BTN_Z": 0x135,
    "BTN_TL": 0x136,
    "BTN_TR": 0x137,
    "BTN_TL2": 0x138,
    "BTN_TR2": 0x139,
    "BTN_SELECT": 0x13A,
    "BTN_START": 0x13B,
    "BTN_MODE": 0x13C,
    "BTN_THUMBL": 0x13D,
    "BTN_THUMBR": 0x13E,
    "BTN_DIGI": 0x140,
    "BTN_TOOL_PEN": 0x140,
    "BTN_TOOL_RUBBER": 0x141,
    "BTN_TOOL_BRUSH": 0x142,
    "BTN_TOOL_PENCIL": 0x143,
    "BTN_TOOL_AIRBRUSH": 0x144,
    "BTN_TOOL_FINGER": 0x145,
    "BTN_TOOL_MOUSE": 0x146,
    "BTN_TOOL_LENS": 0x147,
    "BTN_TOOL_QUINTTAP": 0x148,
    "BTN_STYLUS3": 0x149,
    "BTN_TOUCH": 0x14A,
    "BTN_STYLUS": 0x14B,
    "BTN_STYLUS2": 0x14C,
    "BTN_TOOL_DOUBLETAP": 0x14D,
    "BTN_TOOL_TRIPLETAP": 0x14E,
    "BTN_TOOL_QUADTAP": 0x14F,
    "BTN_WHEEL": 0x150,
    "BTN_GEAR_DOWN": 0x150,
    "BTN_GEAR_UP": 0x151,
    "KEY_OK": 0x160,
    "KEY_SELECT": 0x161,
    "KEY_GOTO": 0x162,
    "KEY_CLEAR": 0x163,
    "KEY_POWER2": 0x164,
    "KEY_OPTION": 0x165,
    "KEY_INFO": 0x166,
    "KEY_TIME": 0x167,
    "KEY_VENDOR": 0x168,
    "KEY_ARCHIVE": 0x169,
    "KEY_PROGRAM": 0x16A,
    "KEY_CHANNEL": 0x16B,
    "KEY_FAVORITES": 0x16C,
    "KEY_EPG": 0x16D,
    "KEY_PVR": 0x16E,
    "KEY_MHP": 0x16F,
    "KEY_LANGUAGE": 0x170,
    "KEY_TITLE": 0x171,
    "KEY_SUBTITLE": 0x172,
    "KEY_ANGLE": 0x173,
    "KEY_FULL_SCREEN": 0x174,
    "KEY_ZOOM": 0x174,
    "KEY_MODE": 0x175,
    "KEY_KEYBOARD": 0x176,
    "KEY_ASPECT_RATIO": 0x177,
    "KEY_SCREEN": 0x177,
    "KEY_PC": 0x178,
    "KEY_TV": 0x179,
    "KEY_TV2": 0x17A,
    "KEY_VCR": 0x17B,
    "KEY_VCR2": 0x17C,
    "KEY_SAT": 0x17D,
    "KEY_SAT2": 0x17E,
    "KEY_CD": 0x17F,
    "KEY_TAPE": 0x180,
    "KEY_RADIO": 0x181,
    "KEY_TUNER": 0x182,
    "KEY_PLAYER": 0x183,
    "KEY_TEXT": 0x184,
    "KEY_DVD": 0x185,
    "KEY_AUX": 0x186,
    "KEY_MP3": 0x187,
    "KEY_AUDIO": 0x188,
    "KEY_VIDEO": 0x189,
    "KEY_DIRECTORY": 0x18A,
    "KEY_LIST": 0x18B,
    "KEY_MEMO": 0x18C,
    "KEY_CALENDAR": 0x18D,
    "KEY_RED": 0x18E,
    "KEY_GREEN": 0x18F,
    "KEY_YELLOW": 0x190,
    "KEY_BLUE": 0x191,
    "KEY_CHANNELUP": 0x192,
    "KEY_CHANNELDOWN": 0x193,
    "KEY_FIRST": 0x194,
    "KEY_LAST": 0x195,
    "KEY_AB": 0x196,
    "KEY_NEXT": 0x197,
    "KEY_RESTART": 0x198,
    "KEY_SLOW": 0x199,
    "KEY_SHUFFLE": 0x19A,
    "KEY_BREAK": 0x19B,
    "KEY_PREVIOUS": 0x19C,
    "KEY_DIGITS": 0x19D,
    "KEY_TEEN": 0x19E,
    "KEY_TWEN": 0x19F,
    "KEY_VIDEOPHONE": 0x1A0,
    "KEY_GAMES": 0x1A1,
    "KEY_ZOOMIN": 0x1A2,
    "KEY_ZOOMOUT": 0x1A3,
    "KEY_ZOOMRESET": 0x1A4,
    "KEY_WORDPROCESSOR": 0x1A5,
    "KEY_EDITOR": 0x1A6,
    "KEY_SPREADSHEET": 0x1A7,
    "KEY_GRAPHICSEDITOR": 0x1A8,
    "KEY_PRESENTATION": 0x1A9,
    "KEY_DATABASE": 0x1AA,
    "KEY_NEWS": 0x1AB,
    "KEY_VOICEMAIL": 0x1AC,
    "KEY_ADDRESSBOOK": 0x1AD,
    "KEY_MESSENGER": 0x1AE,
    "KEY_DISPLAYTOGGLE": 0x1AF,
    "KEY_BRIGHTNESS_TOGGLE": 0x1AF,
    "KEY_SPELLCHECK": 0x1B0,
    "KEY_LOGOFF": 0x1B1,
    "KEY_DOLLAR": 0x1B2,
    "KEY_EURO": 0x1B3,
    "KEY_FRAMEBACK": 0x1B4,
    "KEY_FRAMEFORWARD": 0x1B5,
    "KEY_CONTEXT_MENU": 0x1B6,
    "KEY_MEDIA_REPEAT": 0x1B7,
    "KEY_10CHANNELSUP": 0x1B8,
    "KEY_10CHANNELSDOWN": 0x1B9,
    "KEY_IMAGES": 0x1BA,
    "KEY_NOTIFICATION_CENTER": 0x1BC,
    "KEY_PICKUP_PHONE": 0x1BD,
    "KEY_HANGUP_PHONE": 0x1BE,
    "KEY_DEL_EOL": 0x1C0,
    "KEY_DEL_EOS": 0x1C1,
    "KEY_INS_LINE": 0x1C2,
    "KEY_DEL_LINE": 0x1C3,
    "KEY_FN": 0x1D0,
    "KEY_FN_ESC": 0x1D1,
    "KEY_FN_F1": 0x1D2,
    "KEY_FN_F2": 0x1D3,
    "KEY_FN_F3": 0x1D4,
    "KEY_FN_F4": 0x1D5,
    "KEY_FN_F5": 0x1D6,
    "KEY_FN_F6": 0x1D7,
    "KEY_FN_F7": 0x1D8,
    "KEY_FN_F8": 0x1D9,
    "KEY_FN_F9": 0x1DA,
    "KEY_FN_F10": 0x1DB,
    "KEY_FN_F11": 0x1DC,
    "KEY_FN_F12": 0x1DD,
    "KEY_FN_1": 0x1DE,
    "KEY_FN_2": 0x1DF,
    "KEY_FN_D": 0x1E0,
    "KEY_FN_E": 0x1E1,
    "KEY_FN_F": 0x1E2,
    "KEY_FN_S": 0x1E3,
    "KEY_FN_B": 0x1E4,
    "KEY_FN_RIGHT_SHIFT": 0x1E5,
    "KEY_BRL_DOT1": 0x1F1,
    "KEY_BRL_DOT2": 0x1F2,
    "KEY_BRL_DOT3": 0x1F3,
    "KEY_BRL_DOT4": 0x1F4,
    "KEY_BRL_DOT5": 0x1F5,
    "KEY_BRL_DOT6": 0x1F6,
    "KEY_BRL_DOT7": 0x1F7,
    "KEY_BRL_DOT8": 0x1F8,
    "KEY_BRL_DOT9": 0x1F9,
    "KEY_BRL_DOT10": 0x1FA,
    "KEY_NUMERIC_0": 0x200,
    "KEY_NUMERIC_1": 0x201,
    "KEY_NUMERIC_2": 0x202,
    "KEY_NUMERIC_3": 0x203,
    "KEY_NUMERIC_4": 0x204,
    "KEY_NUMERIC_5": 0x205,
    "KEY_NUMERIC_6": 0x206,
    "KEY_NUMERIC_7": 0x207,
    "KEY_NUMERIC_8": 0x208,
    "KEY_NUMERIC_9": 0x209,
    "KEY_NUMERIC_STAR": 0x20A,
    "KEY_NUMERIC_POUND": 0x20B,
    "KEY_NUMERIC_A": 0x20C,
    "KEY_NUMERIC_B": 0x20D,
    "KEY_NUMERIC_C": 0x20E,
    "KEY_NUMERIC_D": 0x20F,
    "KEY_CAMERA_FOCUS": 0x210,
    "KEY_WPS_BUTTON": 0x211,
    "KEY_TOUCHPAD_TOGGLE": 0x212,
    "KEY_TOUCHPAD_ON": 0x213,
    "KEY_TOUCHPAD_OFF": 0x214,
    "KEY_CAMERA_ZOOMIN": 0x215,
    "KEY_CAMERA_ZOOMOUT": 0x216,
    "KEY_CAMERA_UP": 0x217,
    "KEY_CAMERA_DOWN": 0x218,
    "KEY_CAMERA_LEFT": 0x219,
    "KEY_CAMERA_RIGHT": 0x21A,
    "KEY_ATTENDANT_ON": 0x21B,
    "KEY_ATTENDANT_OFF": 0x21C,
    "KEY_ATTENDANT_TOGGLE": 0x21D,
    "KEY_LIGHTS_TOGGLE": 0x21E,
    "BTN_DPAD_UP": 0x220,
    "BTN_DPAD_DOWN": 0x221,
    "BTN_DPAD_LEFT": 0x222,
    "BTN_DPAD_RIGHT": 0x223,
    "KEY_ALS_TOGGLE": 0x230,
    "KEY_ROTATE_LOCK_TOGGLE": 0x231,
    "KEY_BUTTONCONFIG": 0x240,
    "KEY_TASKMANAGER": 0x241,
    "KEY_JOURNAL": 0x242,
    "KEY_CONTROLPANEL": 0x243,
    "KEY_APPSELECT": 0x244,
    "KEY_SCREENSAVER": 0x245,
    "KEY_VOICECOMMAND": 0x246,
    "KEY_ASSISTANT": 0x247,
    "KEY_KBD_LAYOUT_NEXT": 0x248,
    "KEY_EMOJI_PICKER": 0x249,
    "KEY_DICTATE": 0x24A,
    "KEY_BRIGHTNESS_MIN": 0x250,
    "KEY_BRIGHTNESS_MAX": 0x251,
    "KEY_KBDINPUTASSIST_PREV": 0x260,
    "KEY_KBDINPUTASSIST_NEXT": 0x261,
    "KEY_KBDINPUTASSIST_PREVGROUP": 0x262,
    "KEY_KBDINPUTASSIST_NEXTGROUP": 0x263,
    "KEY_KBDINPUTASSIST_ACCEPT": 0x264,
    "KEY_KBDINPUTASSIST_CANCEL": 0x265,
    "KEY_RIGHT_UP": 0x266,
    "KEY_RIGHT_DOWN": 0x267,
    "KEY_LEFT_UP": 0x268,
    "KEY_LEFT_DOWN": 0x269,
    "KEY_ROOT_MENU": 0x26A,
    "KEY_MEDIA_TOP_MENU": 0x26B,
    "KEY_NUMERIC_11": 0x26C,
    "KEY_NUMERIC_12": 0x26D,
    "KEY_AUDIO_DESC": 0x26E,
    "KEY_3D_MODE": 0x26F,
    "KEY_NEXT_FAVORITE": 0x270,
    "KEY_STOP_RECORD": 0x271,
    "KEY_PAUSE_RECORD": 0x272,
    "KEY_VOD": 0x273,
    "KEY_UNMUTE": 0x274,
    "KEY_FASTREVERSE": 0x275,
    "KEY_SLOWREVERSE": 0x276,
    "KEY_DATA": 0x277,
    "KEY_ONSCREEN_KEYBOARD": 0x278,
    "KEY_PRIVACY_SCREEN_TOGGLE": 0x279,
    "KEY_SELECTIVE_SCREENSHOT": 0x27A,
    "KEY_NEXT_ELEMENT": 0x27B,
    "KEY_PREVIOUS_ELEMENT": 0x27C,
    "KEY_AUTOPILOT_ENGAGE_TOGGLE": 0x27D,
    "KEY_MARK_WAYPOINT": 0x27E,
    "KEY_SOS": 0x27F,
    "KEY_NAV_CHART": 0x280,
    "KEY_FISHING_CHART": 0x281,
    "KEY_SINGLE_RANGE_RADAR": 0x282,
    "KEY_DUAL_RANGE_RADAR": 0x283,
    "KEY_RADAR_OVERLAY": 0x284,
    "KEY_TRADITIONAL_SONAR": 0x285,
    "KEY_CLEARVU_SONAR": 0x286,
    "KEY_SIDEVU_SONAR": 0x287,
    "KEY_NAV_INFO": 0x288,
    "KEY_BRIGHTNESS_MENU": 0x289,
    "KEY_MACRO1": 0x290,
    "KEY_MACRO2": 0x291,
    "KEY_MACRO3": 0x292,
    "KEY_MACRO4": 0x293,
    "KEY_MACRO5": 0x294,
    "KEY_MACRO6": 0x295,
    "KEY_MACRO7": 0x296,
    "KEY_MACRO8": 0x297,
    "KEY_MACRO9": 0x298,
    "KEY_MACRO10": 0x299,
    "KEY_MACRO11": 0x29A,
    "KEY_MACRO12": 0x29B,
    "KEY_MACRO13": 0x29C,
    "KEY_MACRO14": 0x29D,
    "KEY_MACRO15": 0x29E,
    "KEY_MACRO16": 0x29F,
    "KEY_MACRO17": 0x2A0,
    "KEY_MACRO18": 0x2A1,
    "KEY_MACRO19": 0x2A2,
    "KEY_MACRO20": 0x2A3,
    "KEY_MACRO21": 0x2A4,
    "KEY_MACRO22": 0x2A5,
    "KEY_MACRO23": 0x2A6,
    "KEY_MACRO24": 0x2A7,
    "KEY_MACRO25": 0x2A8,
    "KEY_MACRO26": 0x2A9,
    "KEY_MACRO27": 0x2AA,
    "KEY_MACRO28": 0x2AB,
    "KEY_MACRO29": 0x2AC,
    "KEY_MACRO30": 0x2AD,
    "KEY_MACRO_RECORD_START": 0x2B0,
    "KEY_MACRO_RECORD_STOP": 0x2B1,
    "KEY_MACRO_PRESET_CYCLE": 0x2B2,
    "KEY_MACRO_PRESET1": 0x2B3,
    "KEY_MACRO_PRESET2": 0x2B4,
    "KEY_MACRO_PRESET3": 0x2B5,
    "KEY_KBD_LCD_MENU1": 0x2B8,
    "KEY_KBD_LCD_MENU2": 0x2B9,
    "KEY_KBD_LCD_MENU3": 0x2BA,
    "KEY_KBD_LCD_MENU4": 0x2BB,
    "KEY_KBD_LCD_MENU5": 0x2BC,
    "BTN_TRIGGER_HAPPY": 0x2C0,
    "BTN_TRIGGER_HAPPY1": 0x2C0,
    "BTN_TRIGGER_HAPPY2": 0x2C1,
    "BTN_TRIGGER_HAPPY3": 0x2C2,
    "BTN_TRIGGER_HAPPY4": 0x2C3,
    "BTN_TRIGGER_HAPPY5": 0x2C4,
    "BTN_TRIGGER_HAPPY6": 0x2C5,
    "BTN_TRIGGER_HAPPY7": 0x2C6,
    "BTN_TRIGGER_HAPPY8": 0x2C7,
    "BTN_TRIGGER_HAPPY9": 0x2C8,
    "BTN_TRIGGER_HAPPY10": 0x2C9,
    "BTN_TRIGGER_HAPPY11": 0x2CA,
    "BTN_TRIGGER_HAPPY12": 0x2CB,
    "BTN_TRIGGER_HAPPY13": 0x2CC,
    "BTN_TRIGGER_HAPPY14": 0x2CD,
    "BTN_TRIGGER_HAPPY15": 0x2CE,
    "BTN_TRIGGER_HAPPY16": 0x2CF,
    "BTN_TRIGGER_HAPPY17": 0x2D0,
    "BTN_TRIGGER_HAPPY18": 0x2D1,
    "BTN_TRIGGER_HAPPY19": 0x2D2,
    "BTN_TRIGGER_HAPPY20": 0x2D3,
    "BTN_TRIGGER_HAPPY21": 0x2D4,
    "BTN_TRIGGER_HAPPY22": 0x2D5,
    "BTN_TRIGGER_HAPPY23": 0x2D6,
    "BTN_TRIGGER_HAPPY24": 0x2D7,
    "BTN_TRIGGER_HAPPY25": 0x2D8,
    "BTN_TRIGGER_HAPPY26": 0x2D9,
    "BTN_TRIGGER_HAPPY27": 0x2DA,
    "BTN_TRIGGER_HAPPY28": 0x2DB,
    "BTN_TRIGGER_HAPPY29": 0x2DC,
    "BTN_TRIGGER_HAPPY30": 0x2DD,
    "BTN_TRIGGER_HAPPY31": 0x2DE,
    "BTN_TRIGGER_HAPPY32": 0x2DF,
    "BTN_TRIGGER_HAPPY33": 0x2E0,
    "BTN_TRIGGER_HAPPY34": 0x2E1,
    "BTN_TRIGGER_HAPPY35": 0x2E2,
    "BTN_TRIGGER_HAPPY36": 0x2E3,
    "BTN_TRIGGER_HAPPY37": 0x2E4,
    "BTN_TRIGGER_HAPPY38": 0x2E5,
    "BTN_TRIGGER_HAPPY39": 0x2E6,
    "BTN_TRIGGER_HAPPY40": 0x2E7,
    "KEY_MIN_INTERESTING": 113,
    "KEY_MAX": 0x2FF,
    "KEY_CNT": (0x2FF + 1),
    "REL_X": 0x00,
    "REL_Y": 0x01,
    "REL_Z": 0x02,
    "REL_RX": 0x03,
    "REL_RY": 0x04,
    "REL_RZ": 0x05,
    "REL_HWHEEL": 0x06,
    "REL_DIAL": 0x07,
    "REL_WHEEL": 0x08,
    "REL_MISC": 0x09,
    "REL_RESERVED": 0x0A,
    "REL_WHEEL_HI_RES": 0x0B,
    "REL_HWHEEL_HI_RES": 0x0C,
    "REL_MAX": 0x0F,
    "REL_CNT": (0x0F + 1),
    "ABS_X": 0x00,
    "ABS_Y": 0x01,
    "ABS_Z": 0x02,
    "ABS_RX": 0x03,
    "ABS_RY": 0x04,
    "ABS_RZ": 0x05,
    "ABS_THROTTLE": 0x06,
    "ABS_RUDDER": 0x07,
    "ABS_WHEEL": 0x08,
    "ABS_GAS": 0x09,
    "ABS_BRAKE": 0x0A,
    "ABS_HAT0X": 0x10,
    "ABS_HAT0Y": 0x11,
    "ABS_HAT1X": 0x12,
    "ABS_HAT1Y": 0x13,
    "ABS_HAT2X": 0x14,
    "ABS_HAT2Y": 0x15,
    "ABS_HAT3X": 0x16,
    "ABS_HAT3Y": 0x17,
    "ABS_PRESSURE": 0x18,
    "ABS_DISTANCE": 0x19,
    "ABS_TILT_X": 0x1A,
    "ABS_TILT_Y": 0x1B,
    "ABS_TOOL_WIDTH": 0x1C,
    "ABS_VOLUME": 0x20,
    "ABS_PROFILE": 0x21,
    "ABS_MISC": 0x28,
    "ABS_RESERVED": 0x2E,
    "ABS_MT_SLOT": 0x2F,
    "ABS_MT_TOUCH_MAJOR": 0x30,
    "ABS_MT_TOUCH_MINOR": 0x31,
    "ABS_MT_WIDTH_MAJOR": 0x32,
    "ABS_MT_WIDTH_MINOR": 0x33,
    "ABS_MT_ORIENTATION": 0x34,
    "ABS_MT_POSITION_X": 0x35,
    "ABS_MT_POSITION_Y": 0x36,
    "ABS_MT_TOOL_TYPE": 0x37,
    "ABS_MT_BLOB_ID": 0x38,
    "ABS_MT_TRACKING_ID": 0x39,
    "ABS_MT_PRESSURE": 0x3A,
    "ABS_MT_DISTANCE": 0x3B,
    "ABS_MT_TOOL_X": 0x3C,
    "ABS_MT_TOOL_Y": 0x3D,
    "ABS_MAX": 0x3F,
    "ABS_CNT": (0x3F + 1),
    "SW_LID": 0x00,
    "SW_TABLET_MODE": 0x01,
    "SW_HEADPHONE_INSERT": 0x02,
    "SW_RFKILL_ALL": 0x03,
    "SW_RADIO": 0x03,
    "SW_MICROPHONE_INSERT": 0x04,
    "SW_DOCK": 0x05,
    "SW_LINEOUT_INSERT": 0x06,
    "SW_JACK_PHYSICAL_INSERT": 0x07,
    "SW_VIDEOOUT_INSERT": 0x08,
    "SW_CAMERA_LENS_COVER": 0x09,
    "SW_KEYPAD_SLIDE": 0x0A,
    "SW_FRONT_PROXIMITY": 0x0B,
    "SW_ROTATE_LOCK": 0x0C,
    "SW_LINEIN_INSERT": 0x0D,
    "SW_MUTE_DEVICE": 0x0E,
    "SW_PEN_INSERTED": 0x0F,
    "SW_MACHINE_COVER": 0x10,
    "SW_MAX": 0x10,
    "SW_CNT": (0x10 + 1),
    "MSC_SERIAL": 0x00,
    "MSC_PULSELED": 0x01,
    "MSC_GESTURE": 0x02,
    "MSC_RAW": 0x03,
    "MSC_SCAN": 0x04,
    "MSC_TIMESTAMP": 0x05,
    "MSC_MAX": 0x07,
    "MSC_CNT": (0x07 + 1),
    "LED_NUML": 0x00,
    "LED_CAPSL": 0x01,
    "LED_SCROLLL": 0x02,
    "LED_COMPOSE": 0x03,
    "LED_KANA": 0x04,
    "LED_SLEEP": 0x05,
    "LED_SUSPEND": 0x06,
    "LED_MUTE": 0x07,
    "LED_MISC": 0x08,
    "LED_MAIL": 0x09,
    "LED_CHARGING": 0x0A,
    "LED_MAX": 0x0F,
    "LED_CNT": (0x0F + 1),
    "REP_DELAY": 0x00,
    "REP_PERIOD": 0x01,
    "REP_MAX": 0x01,
    "REP_CNT": (0x01 + 1),
    "SND_CLICK": 0x00,
    "SND_BELL": 0x01,
    "SND_TONE": 0x02,
    "SND_MAX": 0x07,
    "SND_CNT": (0x07 + 1),
}
synkeys = {
    0: "SYN_REPORT",
    1: "SYN_CONFIG",
    2: "SYN_MT_REPORT",
    3: "SYN_DROPPED",
    15: "SYN_MAX",
}
abskeys = {
    46: "ABS_RESERVED",
    47: "ABS_MT_SLOT",
    48: "ABS_MT_TOUCH_MAJOR",
    49: "ABS_MT_TOUCH_MINOR",
    50: "ABS_MT_WIDTH_MAJOR",
    51: "ABS_MT_WIDTH_MINOR",
    52: "ABS_MT_ORIENTATION",
    53: "ABS_MT_POSITION_X",
    54: "ABS_MT_POSITION_Y",
    55: "ABS_MT_TOOL_TYPE",
    56: "ABS_MT_BLOB_ID",
    57: "ABS_MT_TRACKING_ID",
    58: "ABS_MT_PRESSURE",
    59: "ABS_MT_DISTANCE",
    60: "ABS_MT_TOOL_X",
    61: "ABS_MT_TOOL_Y",
    63: "ABS_MAX",
}
eventkeysdict = {
    0: "EV_SYN",
    1: "EV_KEY",
    2: "EV_REL",
    3: "EV_ABS",
    4: "EV_MSC",
    5: "EV_SW",
    17: "EV_LED",
    18: "EV_SND",
    20: "EV_REP",
    21: "EV_FF",
    22: "EV_PWR",
    23: "EV_FF_STATUS",
    31: "EV_MAX",
}


def connect_to_adb(adb_path, deviceserial):
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    _ = subprocess.run(
        f"{adb_path} connect {deviceserial}", capture_output=True, shell=False
    )


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def execute_adb_command(
    cmd: str, subcommands: list, exit_keys: str = "ctrl+x", end_of_printline: str = ""
) -> list:
    if isinstance(subcommands, str):
        subcommands = [subcommands]
    elif isinstance(subcommands, tuple):
        subcommands = list(subcommands)
    popen = None

    def run_subprocess(cmd):
        nonlocal popen

        def kill_process():
            nonlocal popen
            try:
                print("Killing the process")
                p = psutil.Process(popen.pid)
                p.kill()
                try:
                    if exit_keys in keyboard__.__dict__["_hotkeys"]:
                        keyboard__.remove_hotkey(exit_keys)
                except Exception:
                    try:
                        keyboard__.unhook_all_hotkeys()
                    except Exception:
                        pass
            except Exception:
                try:
                    keyboard__.unhook_all_hotkeys()
                except Exception:
                    pass

        if exit_keys not in keyboard__.__dict__["_hotkeys"]:
            keyboard__.add_hotkey(exit_keys, kill_process)

        DEVNULL = open(os.devnull, "wb")
        try:
            popen = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                stderr=DEVNULL,
                shell=False,
            )

            for subcommand in subcommands:
                if isinstance(subcommand, bytes):
                    subcommand = subcommand.rstrip(b"\n") + b"\n"

                    subcommand = subcommand.decode("utf-8", "replace")
                else:
                    subcommand = subcommand.rstrip("\n") + "\n"

                popen.stdin.write(subcommand)

            popen.stdin.close()

            for stdout_line in iter(popen.stdout.readline, ""):
                try:
                    yield stdout_line
                except Exception as Fehler:
                    continue
            popen.stdout.close()
            return_code = popen.wait()
        except Exception as Fehler:
            # print(Fehler)
            try:
                popen.stdout.close()
                return_code = popen.wait()
            except Exception as Fehler:
                yield ""

    proxyresults = []
    try:
        for proxyresult in run_subprocess(cmd):
            proxyresults.append(proxyresult)
            print(proxyresult, end=end_of_printline)
    except KeyboardInterrupt:
        try:
            p = psutil.Process(popen.pid)
            p.kill()
            popen = None
        except Exception as da:
            pass
            # print(da)

    try:
        if popen is not None:
            p = psutil.Process(popen.pid)
            p.kill()
    except Exception as da:
        pass

    try:
        if exit_keys in keyboard__.__dict__["_hotkeys"]:
            keyboard__.remove_hotkey(exit_keys)
    except Exception:
        try:
            keyboard__.unhook_all_hotkeys()
        except Exception:
            pass
    return proxyresults


def get_screenwidth(adb_path, deviceserial):
    screenwidth, screenheight = (
        subprocess.run(
            fr'{adb_path} -s {deviceserial} shell dumpsys window | grep cur= |tr -s " " | cut -d " " -f 4|cut -d "=" -f 2',
            shell=True,
            capture_output=True,
        )
        .stdout.decode("utf-8", "ignore")
        .strip()
        .split("x")
    )
    screenwidth, screenheight = int(screenwidth), int(screenheight)
    return screenwidth, screenheight


def fill_df_(df, divider, type_to_repeat=0, code_to_repeat=0):
    diivi = divider
    addtodf = abs(divmod(len(df), diivi)[-1] - diivi)
    first_ = (
        df.loc[(df.aa_type_int == type_to_repeat) & (df.aa_code_int == code_to_repeat)]
        .iloc[-1:]
        .copy()
    )
    addtodataf = []
    for ini, _ in enumerate(range((len(df)), (len(df)) + addtodf)):
        seca = first_.copy()
        seca.index = [_]
        addtodataf.append(seca.copy())
    addtodataf.insert(0, df.copy())
    df = pd.concat(addtodataf).reset_index(drop=True).copy()
    return df


def tempfolder_and_files(fileprefix, numberoffiles=1):
    tempfolder = tempfile.TemporaryDirectory()
    tempfolder.cleanup()
    allfiles = []

    for fi in range(numberoffiles):
        tempfile____txtlist = (
            os.path.join(tempfolder.name, f"{fileprefix}_{str(fi).zfill(8)}")
            .replace("/", os.sep)
            .replace("\\", os.sep)
        ) + ".bin"
        allfiles.append(tempfile____txtlist)
        touch(tempfile____txtlist)

    return allfiles, tempfolder.name.split(os.sep)[-1], tempfolder.name


def copy_bin_files_to_hdd(filepath, data):
    touch(filepath)
    try:
        with open(filepath, mode="wb") as f:
            f.write(data)
        return True
    except Exception:
        pass
    return False


def get_events_as_string(adb_path, deviceserial, exit_keys):
    results = execute_adb_command(
        f"{adb_path} -s {deviceserial} shell",
        ["su -- getevent -tq"],
        exit_keys=exit_keys,
    )
    return results


def record_events_and_convert_to_df(
    adb_path,
    deviceserial,
    bluestacks_divider=32767,
    sdcard="/storage/emulated/0/",
    speed=1,
    exit_keys="ctrl+x",
):
    results = get_events_as_string(adb_path, deviceserial, exit_keys)

    addtoresults = [x for x in results if ": 0000 0000 00000000" in x][-1:] * 4000
    splitted = [regex.split(r"[\]:]?\s+", x.lstrip("[").strip()) for x in addtoresults]
    splitted2 = [
        (str(float(x[0]) + ini / 100)[:12], x[1:]) for ini, x in enumerate(splitted)
    ]
    splitted3 = [
        tuple(
            flatten_everything(
                [
                    "".join(
                        list(
                            reversed("".join(list(reversed(list(str(x[0]))))).zfill(12))
                        )
                    ),
                    x[1:],
                ]
            )
        )
        for x in splitted2
    ]
    splitted4 = [
        "[   " + x[0] + "]" + " " + x[1] + ": " + x[2] + " " + x[3] + " " + x[4]
        for x in splitted3
    ]
    addtoresults = splitted4.copy()
    addtoresults = [
        x.replace(": 0000 0000 00000000", ": 0000 0002 00000000") if ini % 2 == 0 else x
        for ini, x in enumerate(addtoresults)
    ]

    results += addtoresults
    return get_event_to_dataframe(
        adb_path=adb_path,
        eventstring=results,
        deviceserial=deviceserial,
        bluestacks_divider=bluestacks_divider,
        sdcard=sdcard,
        speed=speed,
    )


def adb_path_exists(adb_path, deviceserial, path):
    ex = (
        subprocess.run(
            f"""{adb_path} -s {deviceserial} shell ls {path} > /dev/null 2>&1 && echo "True" || echo "False""",
            shell=False,
            capture_output=True,
        )
        .stdout.decode("utf-8", "ignore")
        .strip()
    )

    if ex == "False":
        return False
    return True


def crate_folder_on_sdcard(
    adb_path,
    deviceserial,
    sdcard="/storage/emulated/0/",
    temfolder_on_sd_card="AUTOMAT",
):
    original_sdcard = sdcard
    tmp_folder_on_sd_card = temfolder_on_sd_card
    pathexits = (
        "/"
        + regex.sub(
            r"[\\/]+", "/", os.path.join(original_sdcard, tmp_folder_on_sd_card),
        ).strip("/")
        + "/"
    )
    if not adb_path_exists(
        adb_path=adb_path, deviceserial=deviceserial, path=pathexits
    ):

        foldertocreate = os.path.normpath(
            os.path.join(os.getcwd(), tmp_folder_on_sd_card)
        )
        if not os.path.exists(foldertocreate):
            os.makedirs(foldertocreate)
        subprocess.run(
            f"{adb_path} -s {deviceserial} push {foldertocreate} {original_sdcard}"
        )
    return pathexits


def execute_event_actions(
    df,
    deviceserial,
    adb_path,
    sdcard="/storage/emulated/0",
    structfolder="struct",
    additional_end_command=True,
    remove_temp_files_from_device=False,
    temfolder_on_sd_card="AUTOMAT",
    sleep_before_additional_command=0.2,
):
    sdcard = crate_folder_on_sdcard(
        adb_path, deviceserial, sdcard=sdcard, temfolder_on_sd_card=temfolder_on_sd_card
    )
    mustcopy = False

    if structfolder == "struct real":
        tmphdd = "struct_real_tmp_hdd"
        successcopy = "aa_copy_struct_real_to_hdd_success"
        copystruct = "aa_copy_struct_real_to_hdd"
        executestruct = "struct_real_copy_dv"
        hddfullpath = "struct_real_tmp_hdd_full_path"
        column_temp_folder = "struct_real_tmp_hdd"
        structfolderand = "struct_real_folder_android"
        if not adb_path_exists(
            adb_path, deviceserial, df.struct_real_file_android.dropna().iloc[0]
        ):
            mustcopy = True

    else:
        tmphdd = "struct_tmp_hdd"
        successcopy = "aa_copy_struct_to_hdd_success"
        copystruct = "aa_copy_struct_to_hdd"
        executestruct = "struct_copy_dv"
        hddfullpath = "struct_tmp_hdd_full_path"
        column_temp_folder = "struct_tmp_hdd"
        structfolderand = "struct_folder_android"

        if not adb_path_exists(
            adb_path, deviceserial, df.struct_file_android.dropna().iloc[0]
        ):
            mustcopy = True

    dfsttemp = df.dropna(subset=tmphdd)
    if mustcopy:
        df.loc[dfsttemp.index, successcopy] = df.dropna(subset=tmphdd)[
            copystruct
        ].apply(lambda x: x())
        subprocess.run(
            fr"{adb_path} -s {deviceserial} push {df[hddfullpath].iloc[0]} {sdcard}"
        )

    execute_adb_command(
        f"{adb_path} -s {deviceserial} shell",
        df.dropna(subset=executestruct)
        .apply(lambda x: f"{x[executestruct]}\nsleep {x['random_sleep']}\n", axis=1)
        .to_list(),
    )
    if remove_temp_files_from_device:
        subprocess.run(
            f"{adb_path} -s {deviceserial} shell rm -r {df[structfolderand].iloc[0]}"
        )
    if additional_end_command:
        letgomouse = df["aa_device"].value_counts().reset_index()["index"].iloc[0]
        basd = f"""
        sleep .01
      sendevent {letgomouse} 0 0 0  
      sendevent {letgomouse} 0 2 0      
      sleep .01
      sendevent {letgomouse} 0 0 0      

          """.strip().splitlines()
        sleep(sleep_before_additional_command)
        execute_adb_command(
            f"{adb_path} -s {deviceserial} shell", [k.strip() for k in basd]
        )


def dataframe_back_to_original_event_list(df):
    eventstring = (
        df.aa_time.apply(
            lambda x: "[   "
            + "".join(
                list(reversed(list("".join(list(reversed(list(str(x))))).zfill(13))))
            )
            + "]"
        )
        + " "
        + df.aa_device
        + ": "
        + df.aa_type_int.apply(lambda x: hex(x)[2:].zfill(4))
        + " "
        + df.aa_code_int.apply(lambda x: hex(x)[2:].zfill(4))
        + " "
        + df.aa_value.astype("string")
    ).to_list()
    return eventstring


def change_playback_speed(
    df,
    adb_path,
    deviceserial,
    bluestacks_divider,
    sdcard,
    temfolder_on_sd_card,
    playback_speed=4,
    folder_to_save=None,
):
    results = dataframe_back_to_original_event_list(df)
    return get_event_to_dataframe(
        eventstring=results,
        adb_path=adb_path,
        deviceserial=deviceserial,
        bluestacks_divider=bluestacks_divider,
        sdcard=sdcard,
        speed=playback_speed,
        folder_to_save=folder_to_save,
        temfolder_on_sd_card=temfolder_on_sd_card,
    )


def get_event_to_dataframe(
    eventstring,
    adb_path,
    deviceserial,
    bluestacks_divider=32767,
    sdcard="/storage/emulated/0/",
    speed=1,
    folder_to_save=None,
    temfolder_on_sd_card="AUTOMAT",
):
    sdcard = crate_folder_on_sdcard(
        adb_path, deviceserial, sdcard=sdcard, temfolder_on_sd_card=temfolder_on_sd_card
    )

    sdcard = "/" + sdcard.strip("/") + "/"

    if isinstance(eventstring, str):
        eventstring = eventstring.splitlines()

    results = eventstring
    df2 = (
        pd.DataFrame(
            [
                regex.split(r"[\]:]?\s+", x.lstrip("[").strip())
                for x in results
                if x.startswith("[ ")
            ]
        )
        .dropna()
        .reset_index(drop=True)
    )
    df2 = df2.dropna().reset_index(drop=True)
    df2.columns = ["aa_time", "aa_device", "aa_type_int", "aa_code_int", "aa_value"]
    df2["aa_type_int"] = int_array(df2["aa_type_int"], 16)
    df2["aa_code_int"] = int_array(df2["aa_code_int"], 16)
    df2["aa_value_int"] = int_array(df2["aa_value"], 16)

    keycodeslinux_around = {v: k for k, v in keycodeslinux.items()}
    df2["aa_type"] = df2["aa_type_int"].map(lambda _: keycodeslinux_around.get(_))
    df2["aa_code"] = df2["aa_code_int"].map(lambda _: keycodeslinux_around.get(_))

    df2.aa_code = df2.aa_code_int.map(
        lambda x: abskeys.get(x) if abskeys.get(x) is not None else synkeys.get(x)
    )
    df2.aa_type = df2.aa_type_int.map(lambda x: eventkeysdict.get(x))

    df2.aa_time = df2.aa_time.astype("string").astype("Float64")
    results_ = execute_adb_command(
        f"{adb_path} -s {deviceserial} shell", ["su -- getevent -S"]
    )
    devicesx = [
        x.split(":", maxsplit=1)[-1].strip().strip("""\"'""").strip()
        for x in results_
        if regex.search(r"^((?:add\s+device)|(?:\s+name:))", x)
    ]
    devicesx = {k: v for k, v in (chunked(devicesx, 2))}
    df2["aa_device_name"] = df2["aa_device"].map(lambda x: devicesx.get(x))
    df2 = df2.filter(
        [
            "aa_time",
            "aa_device",
            "aa_type",
            "aa_code",
            "aa_value",
            "aa_device_name",
            "aa_value_int",
            "aa_code_int",
            "aa_type_int",
        ]
    )

    df = df2.copy()
    df.loc[:, "aa_time_difference_start"] = df.aa_time - df.aa_time.iloc[0]
    df.loc[:, "aa_time_diff_actions"] = df.aa_time.diff(-1).abs()

    screenwidth, screenheight = get_screenwidth(f"{adb_path}", deviceserial)

    df.loc[:, "aa_real_coords"] = 0
    df.loc[(df.aa_value_int > 0) & (df.aa_code_int == 53), "aa_real_coords"] = (
        df.loc[(df.aa_value_int > 0) & (df.aa_code_int == 53), "aa_value_int"]
        * screenwidth
        / bluestacks_divider
    )
    df.loc[(df.aa_value_int > 0) & (df.aa_code_int == 54), "aa_real_coords"] = (
        df.loc[(df.aa_value_int > 0) & (df.aa_code_int == 54), "aa_value_int"]
        * screenheight
        / bluestacks_divider
    )
    df.aa_real_coords = df.aa_real_coords.astype(np.uint16)
    df.loc[:, "aa_send_event"] = (
        "sendevent "
        + df.aa_device
        + " "
        + df.aa_type_int.astype("string")
        + " "
        + df.aa_code_int.astype("string")
        + " "
        + df.aa_value_int.astype("string")
    )
    df.loc[:, "aa_send_event_real_ccords"] = (
        "sendevent "
        + df.aa_device
        + " "
        + df.aa_type_int.astype("string")
        + " "
        + df.aa_code_int.astype("string")
        + " "
        + df.aa_real_coords.astype("string")
    )
    df = df.dropna().reset_index(drop=True)
    df["aa_time_new"] = 1

    df = df.dropna().reset_index(drop=True)
    FORMAT = "llHHI"
    EVENT_SIZE = struct.calcsize(FORMAT)
    df = fill_df_(df, int(speed * 4))
    df.aa_value_int = df.aa_value_int.astype(np.uint64)
    df["aa_struct"] = df.apply(
        lambda x: struct.pack(
            FORMAT, 1, 2, int(x.aa_type_int), int(x.aa_code_int), int(x.aa_value_int),
        ),
        axis=1,
    )
    df["aa_struct_real"] = df.apply(
        lambda x: struct.pack(
            FORMAT, 3, 2, int(x.aa_type_int), int(x.aa_code_int), int(x.aa_real_coords),
        ),
        axis=1,
    )
    df["aa_struct_size"] = EVENT_SIZE
    df["aa_struct_real_size"] = EVENT_SIZE

    alltog = [
        df.loc[x[0] : x[-1] - 1, :] if x != -1 else df.loc[x[0] :, :]
        for x in (
            windowed(
                df.loc[df.aa_value_int > 0, "aa_value_int"].index.to_list(),
                int(speed * 4) - 1,
                fillvalue=-1,
                step=int(speed * 4) - 2,
            )
        )
    ]
    df["aa_struct_together"] = pd.NA
    for _ in alltog:
        try:
            df.at[_.index[0], "aa_struct_together"] = b"".join(_.aa_struct.to_list())
        except Exception:
            pass

    df["aa_struct_real_together"] = pd.NA
    for _ in alltog:
        try:
            df.at[_.index[0], "aa_struct_real_together"] = b"".join(
                _.aa_struct_real.to_list()
            )
        except Exception:
            pass

    locator = df.loc[~df.aa_struct_together.isna()]
    allfiles, tempfolder, tempfolder_name = tempfolder_and_files(
        fileprefix="struct", numberoffiles=len(locator)
    )
    df.loc[:, "struct_tmp_hdd_full_path"] = tempfolder_name

    df.loc[:, "struct_tmp_hdd"] = pd.NA
    df.loc[locator.index, "struct_tmp_hdd"] = allfiles
    df.loc[:, "struct_tmp_folder"] = tempfolder
    df["struct_filename"] = (
        df.struct_tmp_hdd.str.split(os.sep, expand=True).__array__().T[-1]
    )

    allfiles, tempfolder, tempfolder_name = tempfolder_and_files(
        fileprefix="structreal", numberoffiles=len(locator)
    )
    df.loc[:, "struct_real_tmp_hdd_full_path"] = tempfolder_name

    df.loc[:, "struct_real_tmp_hdd"] = pd.NA
    df.loc[locator.index, "struct_real_tmp_hdd"] = allfiles
    df.loc[:, "struct_real_tmp_folder"] = tempfolder
    df["struct_real_filename"] = (
        df.struct_real_tmp_hdd.str.split(os.sep, expand=True).__array__().T[-1]
    )
    dfgoa = df.dropna(subset="aa_struct_together")
    df["struct_copy_dv"] = pd.NA
    df.loc[:, "aa_struct_size"] = len(dfgoa.aa_struct_together.iloc[0])
    df.loc[:, "aa_struct_real_size"] = len(dfgoa.aa_struct_real_together.iloc[0])

    df.loc[dfgoa.index, "struct_copy_dv"] = dfgoa.apply(
        lambda x: f"dd bs={int(x.aa_struct_size)} if={sdcard}{x.struct_tmp_folder}/{x.struct_filename} of={x.aa_device}",
        axis=1,
    ).copy()

    dfgoa = df.dropna(subset="aa_struct_real_together")
    df["struct_real_copy_dv"] = pd.NA
    df.loc[dfgoa.index, "struct_real_copy_dv"] = dfgoa.apply(
        lambda x: f"dd bs={int(x.aa_struct_real_size)} if={sdcard}{x.struct_real_tmp_folder}/{x.struct_real_filename} of={x.aa_device}",
        axis=1,
    ).copy()
    df["random_sleep"] = df.aa_time_diff_actions.copy()

    dfsttemp = df.dropna(subset="struct_tmp_hdd")
    df.loc[dfsttemp.index, "aa_copy_struct_to_hdd"] = dfsttemp.apply(
        lambda x: FlexiblePartial(
            copy_bin_files_to_hdd,
            True,
            filepath=x.struct_tmp_hdd,
            data=x.aa_struct_together,
        ),
        axis=1,
    )
    df.loc[dfsttemp.index, "aa_copy_struct_real_to_hdd"] = dfsttemp.apply(
        lambda x: FlexiblePartial(
            copy_bin_files_to_hdd,
            True,
            filepath=x.struct_real_tmp_hdd,
            data=x.aa_struct_real_together,
        ),
        axis=1,
    )

    timedifference = df.loc[df.aa_time_diff_actions > 0].copy()
    timedifference.loc[:, "old_index"] = timedifference.index.__array__().copy()
    structnona = df.aa_struct_together.dropna().to_frame().copy()
    structnona.loc[:, "old_index"] = structnona.index.__array__().copy()

    for _ in range(len(structnona)):
        try:
            max_neighbour = find_nearest(
                timedifference.old_index, structnona.old_index.iloc[_ + speed - 1]
            )

            sleepva = df.loc[max_neighbour].aa_time_diff_actions
            df.at[max_neighbour, "random_sleep"] = sleepva
        except Exception:
            pass
    df.loc[:, "struct_folder_android"] = regex.findall(
        r"(?<=if=).*?(?=/[^/]+\.bin\b)", df.struct_copy_dv.dropna().iloc[0]
    )[0]
    df.loc[:, "struct_real_folder_android"] = regex.findall(
        r"(?<=if=).*?(?=/[^/]+\.bin\b)", df.struct_real_copy_dv.dropna().iloc[0]
    )[0]

    extractstring = (
        df["struct_copy_dv"]
        .str.extract(r"(?<=if=)(?P<struct_file_android>.*?\.bin)\b")
        .copy()
    )
    df = pd.concat([df, extractstring], axis=1).copy()

    extractstring = (
        df["struct_real_copy_dv"]
        .str.extract(r"(?<=if=)(?P<struct_real_file_android>.*?\.bin)\b")
        .copy()
    )
    df = pd.concat([df, extractstring], axis=1).copy()

    if folder_to_save is not None:

        touch(folder_to_save)
        df.to_pickle(folder_to_save)
    return df


class GetEventSendEvent:
    def __init__(
        self,
        adb_path,
        deviceserial,
        sdcard="/storage/emulated/0/",
        temfolder_on_sd_card="AUTOMAT",
        bluestacks_divider=32767,
        exit_keys="ctrl+x",
    ):
        self.adb_path = adb_path
        self.deviceserial = deviceserial
        self.sdcard = sdcard
        self.bluestacks_divider = bluestacks_divider
        self.exit_keys = exit_keys
        self.temfolder_on_sd_card = temfolder_on_sd_card

    def connect_to_adb(self):
        connect_to_adb(
            adb_path=self.adb_path, deviceserial=self.deviceserial,
        )
        return self

    def record_events_and_convert_to_df(self, playbackspeed=2):
        df = record_events_and_convert_to_df(
            deviceserial=self.deviceserial,
            adb_path=self.adb_path,
            bluestacks_divider=self.bluestacks_divider,
            sdcard=self.sdcard,
            speed=playbackspeed,
            exit_keys=self.exit_keys,
        )
        return df

    def execute_recorded_events(
        self,
        df,
        structfolder="struct",
        additional_end_command=True,
        remove_temp_files_from_device=False,
    ):
        execute_event_actions(
            df=df,
            deviceserial=self.deviceserial,
            adb_path=self.adb_path,
            sdcard=self.sdcard,
            structfolder=structfolder,
            additional_end_command=additional_end_command,
            remove_temp_files_from_device=remove_temp_files_from_device,
            temfolder_on_sd_card=self.temfolder_on_sd_card,
        )

    def change_playback_speed(self, df, playback_speed=8):
        return change_playback_speed(
            df,
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            bluestacks_divider=self.bluestacks_divider,
            sdcard=self.sdcard,
            temfolder_on_sd_card=self.temfolder_on_sd_card,
            playback_speed=playback_speed,
            folder_to_save=None,
        )

    def save_recorded_data_on_hdd(self, df, path):
        touch(path)
        toge = "\n".join(dataframe_back_to_original_event_list(df)).strip()
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(toge)

    def load_recoded_data(self, path, playback_speed=4):
        with open(path, mode="r", encoding="utf-8") as f:
            data = f.read()
        data = data.strip()
        return get_event_to_dataframe(
            eventstring=data,
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            bluestacks_divider=self.bluestacks_divider,
            sdcard=self.sdcard,
            speed=playback_speed,
            folder_to_save=None,
            temfolder_on_sd_card=self.temfolder_on_sd_card,
        )
