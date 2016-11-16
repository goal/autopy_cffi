#
#

CC = D:\MingW\bin\gcc.exe -Wall -std=c99
RM = D:\MinGW\git\usr\bin\rm.exe
FLAGS = #-ldl

INCLUDES = -ID:\MinGW\include
LIB = -LD:\MinGW\lib

.PHONY: all mouse clean

all: mouse color alert key screen #bitmap

mouse: deadbeef_rand.o mouse.o screen.o
	$(CC) -shared deadbeef_rand.o mouse.o screen.o $(FLAGS) -o $@.dll

color: color.o
	$(CC) -shared color.o $(FLAGS) -o $@.dll

alert: alert.o
	$(CC) -shared alert.o $(FLAGS) -o $@.dll

key: keypress.o keycode.o deadbeef_rand.o
	$(CC) -shared keypress.o keycode.o deadbeef_rand.o $(FLAGS) -o $@.dll

#MMBitmap.o bmp_io.o io.o png_io.o
screen: screen.o MMBitmap.o screengrab.o base64.o io.o screengrab.o bmp_io.o \
	png_io.o str_io.o screen.o MMBitmap.o snprintf.o \
	pasteboard.o color_find.o bitmap_find.o UTHashTable.o MMPointArray.o zlib_util.o bitmap.o
	$(CC) -shared $^ $(FLAGS) -lgdi32 -lpng -lz -o $@.dll

bitmap: base64.o io.o screengrab.o bmp_io.o png_io.o str_io.o screen.o MMBitmap.o snprintf.o\
	pasteboard.o color_find.o bitmap_find.o UTHashTable.o MMPointArray.o zlib_util.o bitmap.o
	$(CC) -shared $^ -lgdi32 $(FLAGS) -lpng -lz -o $@.dll

%.o: %.c
	$(CC) -c -o $@ $< $(INCLUDES) $(LIB)

clean:
	-$(RM) -f *.o *.dll *.so