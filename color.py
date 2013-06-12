#!/usr/bin/env python
#encoding=utf-8

from cffi import FFI


ffi = FFI()

ffi.cdef("""
uint8_t *color_hex_to_rgb(uint32_t h);
uint32_t color_rgb_to_hex(uint8_t r, uint8_t g, uint8_t b);
""")

_color = ffi.dlopen("color.dll")


def rgb_to_hex(r, g, b):
	return _color.color_rgb_to_hex(r, g, b)

def hex_to_rgb(h):
	cData = _color.color_hex_to_rgb(h)
	return cData[0], cData[1], cData[2]


if __name__ == '__main__':
	print(rgb_to_hex(1, 1, 1))
	print(hex_to_rgb(256))