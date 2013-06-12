#!/usr/bin/env python
#encoding=utf-8

import sys
from cffi import FFI


ffi = FFI()

if sys.platform in ("win32", "cygwin"):
	ifdefstr = 	"""

	enum _MMKeyCode {
		K_BACKSPACE = 8,
		K_DELETE = 46,
		K_RETURN = 13,
		K_ESCAPE = 0x1B,
		K_UP = 38,
		K_DOWN = 40,
		K_RIGHT = 39,
		K_LEFT = 37,
		K_HOME = 36,
		K_END = 35,
		K_PAGEUP = 33,
		K_PAGEDOWN = 34,
		K_F1 = 0x70,
		K_F2 = 0x71,
		K_F3 = 0x72,
		K_F4 = 0x73,
		K_F5 = 0x74,
		K_F6 = 0x75,
		K_F7 = 0x76,
		K_F8 = 0x77,
		K_F9 = 0x709,
		K_F10 = 0x700,
		K_F11 = 0x701,
		K_F12 = 0x702,
		K_META = 0x5B,
		K_CONTROL = 17,
		K_SHIFT = 16,
		K_ALT = 18,
		K_CAPSLOCK = 20
	};

	enum _MMKeyFlags {
		MOD_NONE = 0,
		MOD_ALT = 1,
		MOD_CONTROL = 2,
		MOD_SHIFT = 4,
		MOD_META = 8
	};

	typedef unsigned int MMKeyFlags;
	typedef int MMKeyCode;"""
elif sys.platform == "darwin":
	ifdefstr = """
	#include <Carbon/Carbon.h>
	#include <ApplicationServices/ApplicationServices.h>
	enum _MMKeyFlags {
		MOD_NONE = 0,
		MOD_META = kCGEventFlagMaskCommand,
		MOD_ALT = kCGEventFlagMaskAlternate,
		MOD_CONTROL = kCGEventFlagMaskControl,
		MOD_SHIFT = kCGEventFlagMaskShift
	};

	typedef CGEventFlags MMKeyFlags;
	typedef CGKeyCode MMKeyCode;"""
elif sys.platform == "linux":
	ifdefstr = """
	#include <X11/Xutil.h>
	enum _MMKeyFlags {
		MOD_NONE = 0,
		MOD_META = Mod4Mask,
		MOD_ALT = Mod1Mask,
		MOD_CONTROL = ControlMask,
		MOD_SHIFT = ShiftMask
	};

	typedef unsigned int MMKeyFlags;
	typedef KeySym MMKeyCode;"""

cdefstr = ifdefstr + """
void toggleKeyCode(MMKeyCode code, const bool down, MMKeyFlags flags);
void tapKeyCode(MMKeyCode code, MMKeyFlags flags);
void toggleKey(char c, const bool down, MMKeyFlags flags);
void tapKey(char c, MMKeyFlags flags);
void typeString(const char *str);
void typeStringDelayed(const char *str, const unsigned cpm);
"""

ffi.cdef(cdefstr)
_key = ffi.dlopen("key.dll")

MOD_NONE = _key.MOD_NONE
MOD_META = _key.MOD_META
MOD_ALT = _key.MOD_ALT
MOD_CONTROL = _key.MOD_CONTROL
MOD_SHIFT = _key.MOD_SHIFT
K_BACKSPACE = _key.K_BACKSPACE
K_DELETE = _key.K_DELETE
K_RETURN = _key.K_RETURN
K_ESCAPE = _key.K_ESCAPE
K_UP = _key.K_UP
K_DOWN = _key.K_DOWN
K_RIGHT = _key.K_RIGHT
K_LEFT = _key.K_LEFT
K_HOME = _key.K_HOME
K_END = _key.K_END
K_PAGEUP = _key.K_PAGEUP
K_PAGEDOWN = _key.K_PAGEDOWN
K_F1 = _key.K_F1
K_F2 = _key.K_F2
K_F3 = _key.K_F3
K_F4 = _key.K_F4
K_F5 = _key.K_F5
K_F6 = _key.K_F6
K_F7 = _key.K_F7
K_F8 = _key.K_F8
K_F9 = _key.K_F9
K_F10 = _key.K_F10
K_F11 = _key.K_F11
K_F12 = _key.K_F12
K_META = _key.K_META
K_ALT = _key.K_ALT
K_CONTROL = _key.K_CONTROL
K_SHIFT = _key.K_SHIFT
K_CAPSLOCK = _key.K_CAPSLOCK

ENC = sys.getdefaultencoding()

def toggle(key, down_or_up, modifiers=0):
	if isinstance(key, int):
		_key.toggleKeyCode(key, bool(down_or_up), modifiers)
	if isinstance(key, str):
		key = key.encode(ENC)
		_key.toggleKey(key, bool(down_or_up), modifiers)


def key_tap(key, modifiers=0):
	if isinstance(key, int):
		_key.tapKeyCode(key, modifiers)
	if isinstance(key, str):
		key = key.encode(ENC)
		_key.tapKey(key, modifiers)


def type_string(kstr, wpm=0):
	kstr = kstr.encode(ENC)
	if wpm == 0:
		_key.typeString(kstr)
	else:
		_key.typeStringDelayed(kstr, int(5.1 * wpm))


if __name__ == '__main__':
	toggle('s', 1, MOD_META)
	toggle('s', 0, MOD_META)

	import time
	time.sleep(1)

	key_tap('b')

	type_string("ytestring")