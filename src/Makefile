#
#

CC = C:\MingW\bin\gcc.exe

.PHONY: all mouse clean

all: mouse color alert key screen bitmap

mouse: deadbeef_rand.o mouse.o screen.o
	$(CC) -shared deadbeef_rand.o mouse.o screen.o -ldl -o $@.dll

color: color.o
	$(CC) -shared color.o -ldl -o $@.dll

alert: alert.o
	$(CC) -shared alert.o -ldl -o $@.dll

key: keypress.o keycode.o deadbeef_rand.o
	$(CC) -shared keypress.o keycode.o deadbeef_rand.o -ldl -o $@.dll

#MMBitmap.o bmp_io.o io.o png_io.o
screen: screen.o MMBitmap.o screengrab.o
	$(CC) -shared screengrab.o screen.o MMBitmap.o -ldl -lgdi32 -o $@.dll

bitmap: base64.o io.o screengrab.o bmp_io.o png_io.o str_io.o screen.o MMBitmap.o snprintf.o\
	pasteboard.o color_find.o bitmap_find.o UTHashTable.o MMPointArray.o zlib_util.o bitmap.o
	$(CC) -shared base64.o io.o screengrab.o bmp_io.o png_io.o\
		str_io.o screen.o pasteboard.o color_find.o bitmap_find.o bitmap.o\
		UTHashTable.o MMPointArray.o zlib_util.o MMBitmap.o snprintf.o -lgdi32 -ldl -lpng -lz -o $@.dll

%.o: %.c
	$(CC) -c -o $@ $<

clean:
	-rm -f *.o *.dll *.so