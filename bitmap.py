#!/usr/bin/env python
# encoding=utf-8

import os
import sys
from cffi import FFI
import screen


ffi = FFI()

ffi.cdef("""
	typedef uint32_t MMRGBHex;

	struct _MMPoint {
		size_t x;
		size_t y;
	};
	
	typedef struct _MMPoint MMPoint;

	struct _MMSize {
		size_t width;
		size_t height;
	};

	typedef struct _MMSize MMSize;

	struct _MMRect {
		MMPoint origin;
		MMSize size;
	};

	typedef struct _MMRect MMRect;

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

	void bitmap_dealloc(MMBitmapRef bitmap);
	void destroyMMBitmap(MMBitmapRef bitmap);

	bool bitmap_ready(MMBitmapRef bitmap);

	MMBitmapRef bitmap_open(const char *path, const char *format);
	bool bitmap_save(MMBitmapRef bitmap, const char *path, const char *format);

	bool bitmap_point_in_bounds(MMBitmapRef bitmap, MMPoint point);
	bool bitmap_to_string(MMBitmapRef bitmap, char *buf);
	MMBitmapRef bitmap_from_string(const char *str);
	MMRGBHex Bitmap_get_color(MMBitmapRef bitmap, MMPoint point);
	bool bitmap_copy_to_pboard(MMBitmapRef bitmap);
	MMBitmapRef bitmap_get_portion(MMBitmapRef bitmap, MMRect rect);
	int bitmap_count_of_color(MMBitmapRef bitmap, MMRGBHex color, float tolerance);
	MMPoint bitmap_find_bitmap(MMBitmapRef bitmap, MMBitmapRef sbitmap, float tolerance);
	int bitmap_count_of_bitmap(MMBitmapRef bitmap, MMBitmapRef sbitmap, float tolerance);
	MMPoint bitmap_find_color(MMBitmapRef bitmap, MMRGBHex color, float tolerance);
	// size of list should be larger than sizeof(MMPoint) * count
	MMPoint *bitmap_find_every_color(MMBitmapRef bitmap, MMRGBHex color, float tolerance, MMPoint *list);
	MMPoint *bitmap_find_every_bitmap(MMBitmapRef bitmap, MMBitmapRef sbitmap, float tolerance, MMPoint *list);

""")

_bitmap = ffi.dlopen("bitmap.dll")


class Bitmap():

    def __init__(self, bmp_ref):
        self.enc = sys.getfilesystemencoding()

        self.bmp_ref = bmp_ref
        self.height = bmp_ref.height
        self.width = bmp_ref.width

    # def __del__(self):
    #	_bitmap.bitmap_dealloc(self.bmp_ref)

    def bitmap_ready(self):
        return _bitmap.bitmap_ready(self.bmp_ref)

    def save(self, filepath, format=ffi.NULL):
        filepath = filepath.encode(self.enc)
        format = format.encode(self.enc) if format != ffi.NULL else format
        return _bitmap.bitmap_save(self.bmp_ref, filepath, format)

    @classmethod
    def open(self, _filepath, format=ffi.NULL):
        enc = sys.getfilesystemencoding()
        filepath = _filepath.encode(enc)
        if not os.path.exists(filepath):
            raise FileNotFoundError("%s not found!" % _filepath)
        format = format.encode(enc) if format != ffi.NULL else format
        bmp_ref = _bitmap.bitmap_open(filepath, format)
        return Bitmap(bmp_ref)

    def point_in_bounds(self, x, y):
        return _bitmap.bitmap_point_in_bounds(self.bmp_ref, [x, y])

    def to_string(self):
        _s = ffi.gc(
            _bitmap.new("char[]", self.width * self.height), _bitmap.free)
        if _bitmap.bitmap_to_string(self.bmp_ref, _s):
            return str(_s)
        else:
            return ""

    @classmethod
    def from_string(self, _s):
        _bitmap_ref = _bitmap.bitmap_from_string(_s)
        return Bitmap(_bitmap_ref)

    def get_color(self, x, y):
        return _bitmap.get_color(self.bmp_ref, [x, y])

    def copy_to_pboard(self):
        return bool(_bitmap.bitmap_copy_to_pboard(self.bmp_ref))

    def get_portion(self, x, y, w, h):
        _bitmap_ref = _bitmap.bitmap_get_portion(self.bmp_ref, [[x, y], w, h])
        return Bitmap(_bitmap_ref)

    def count_of_color(self, color, tolerance=0.0):
        return _bitmap.bitmap_count_of_color(self.bmp_ref, color, tolerance)

    def count_of_bitmap(self, color, bmp, tolerance=0.0):
        return _bitmap.bitmap_count_of_bitmap(self.bmp_ref, bmp.bmp_ref, tolerance)

    def find_color(self, color, tolerance=0.0):
        point = _bitmap.bitmap_find_color(self.bmp_ref, color, tolerance)
        return point.x, point.y

    def find_bitmap(self, bmp, tolerance=0.0):
        point = _bitmap.bitmap_find_bitmap(
            self.bmp_ref, bmp.bmp_ref, tolerance)
        return point.x, point.y

    def find_every_color(self, color, tolerance=0.0):
        n = self.count_of_color(color, tolerance)
        size = ffi.sizeof("MMPoint")
        point_ptr = ffi.gc(_bitmap.new("MMPoint[]", n * size), _bitmap.free)
        point_ptr = _bitmap.bitmap_find_every_color(
            self.bmp_ref, color, tolerance, point_ptr)
        _list_result = []
        for i in range(n):
            point = point_ptr[i]
            _list_result.append((point.x, point.y))

        return tuple(_list_result)

    def find_every_bitmap(self, bmp, tolerance=0.0):
        n = self.count_of_bitmap(bmp, tolerance)
        size = ffi.sizeof("MMPoint")
        point_ptr = ffi.gc(_bitmap.new("MMPoint[]", n * size), _bitmap.free)
        point_ptr = _bitmap.bitmap_find_every_bitmap(
            self.bmp_ref, bmp.bmp_ref, tolerance, point_ptr)
        _list_result = []
        for i in range(n):
            point = point_ptr[i]
            _list_result.append((point.x, point.y))

        return tuple(_list_result)


if __name__ == '__main__':
    a = screen.capture_screen()
    print(a.height)
    print(a.save("hhh.png"))
