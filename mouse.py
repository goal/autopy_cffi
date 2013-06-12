#!/usr/bin/env python
#encoding=utf-8

from cffi import FFI


ffi = FFI()

ffi.cdef("""
struct _MMPoint {
	size_t x;
	size_t y;
};
typedef struct _MMPoint MMPoint;

enum _MMMouseButton {
	LEFT_BUTTON = 1,
	CENTER_BUTTON = 2,
	RIGHT_BUTTON = 3
};
typedef unsigned int MMMouseButton;

void moveMouse(MMPoint point);
bool smoothlyMoveMouse(MMPoint point);
MMPoint getMousePos(void);
void toggleMouse(bool down, MMMouseButton button);
void clickMouse(MMMouseButton button);
""")

_mouse = ffi.dlopen("mouse.dll")

LEFT_BUTTON = _mouse.LEFT_BUTTON
CENTER_BUTTON = _mouse.CENTER_BUTTON
RIGHT_BUTTON = _mouse.RIGHT_BUTTON

def move(x, y):
	return _mouse.moveMouse([x, y])

def smooth_move(x, y):
	return bool(_mouse.smoothlyMoveMouse([x, y]))

def get_pos():
	cData = _mouse.getMousePos()
	return cData.x, cData.y

def toggle(down, button=LEFT_BUTTON):
	return _mouse.toggleMouse(down, button)

def click(button):
	return _mouse.clickMouse(button)


def test1():
	import time
	move(60, 70)
	time.sleep(2)

	print(smooth_move(1360, 700))
	time.sleep(2)

	print(get_pos())

	toggle(1, RIGHT_BUTTON)
	time.sleep(2)

	clicke(LEFT_BUTTON)

def my_smooth_move(x, y):
	ex, ey = point
	sx, sy = get_pos()
	h = (ey - sy) / (ex - sx)
	step = -1 if ex < sx else 1

	while ex != sx:
		sx += step
		sy += h * step

		if sx < 0 or sx > 1366 or sy < 0 or sy > 768:
			return False

		move(sx, int(sy))
		import time
		time.sleep(0.001)

	return True

if __name__ == '__main__':
	print(my_smooth_move(100, 200))