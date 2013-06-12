#!/usr/bin/env python
#encoding=utf-8

import sys
from cffi import FFI

import bitmap


ffi = FFI()

ffi.cdef("""
	struct _MMSize {
		size_t width;
		size_t height;
	};

	typedef struct _MMSize MMSize;
	struct _MMPoint {
		size_t x;
		size_t y;
	};
	typedef struct _MMPoint MMPoint;
	typedef uint32_t MMRGBHex;
	struct _MMRect {
		MMPoint origin;
		MMSize size;
	};

	typedef struct _MMRect MMRect;
	MMSize getMainDisplaySize(void);
	MMRGBHex getScreenColor(MMPoint point);

	struct _MMBitmap {
		uint8_t *imageBuffer;  /* Pixels stored in Quad I format; i.e., origin is in
		                        * top left. Length should be height * bytewidth. */
		size_t width;          /* Never 0, unless image is NULL. */
		size_t height;         /* Never 0, unless image is NULL. */
		size_t bytewidth;      /* The aligned width (width + padding). */
		uint8_t bitsPerPixel;  /* Should be either 24 or 32. */
		uint8_t bytesPerPixel; /* For convenience; should be bitsPerPixel / 8. */
	};

	typedef struct _MMBitmap MMBitmap;
	typedef MMBitmap *MMBitmapRef;

	MMBitmapRef copyMMBitmapFromDisplayInRect(MMRect rect);
""")

_screen = ffi.dlopen("screen.dll")


def get_size():
	cData = _screen.getMainDisplaySize()
	return cData.width, cData.height

def point_visible(x, y):
	mx, my = get_size()
	return (x < mx) and (y < my)

def get_color(x, y):
	return _screen.getScreenColor([x, y])

def capture_screen(rect=None):
	"""
	for example:
	rect = ((0, 0), (800, 800))

	if rect is None, the entire screen is captured instead.
	"""

	w, h = get_size()
	if not rect:
		rect = ((0, 0), (w, h))

	if not point_visible(rect[0][0], rect[0][1]) or rect[0][0]+rect[1][0] > w or rect[0][1]+rect[1][1] > h:
		raise ValueError("Rect out of bounds")

	bmp_ref = _screen.copyMMBitmapFromDisplayInRect(rect)

	if not bmp_ref or not bmp_ref.imageBuffer:
		raise OSError("Could not copy RGB data from display")

	return bitmap.Bitmap(bmp_ref)

if __name__ == '__main__':
	print(get_size())
	print(point_visible(1, 2))
	print(point_visible(1366, 768))
	print(point_visible(1365, 767))

	print(get_color(200, 200))