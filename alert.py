#!/usr/bin/env python
#encoding=utf-8

import sys
from cffi import FFI


ffi = FFI()

ffi.cdef("""
int showAlert(const char *title, const char *msg, const char *defaultButton,
              const char *cancelButton);
""")

_alert = ffi.dlopen("alert.dll")

def alert(msg, title="AutoPy Alert", default_button="OK", cancel_button=""):
	enc = sys.getdefaultencoding()
	args = (i.encode(enc) for i in (msg, title, default_button, cancel_button))
	result = _alert.showAlert(*args)

	if result == 0:
		return True
	elif result == 1:
		return False
	else:
		print("Could not display alert", file=sys.stderr)
		return None


if __name__ == '__main__':
	print(alert("Hello world!", "I am super man, are you outman?", default_button="Yes", \
		cancel_button="No"))