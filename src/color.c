#include "rgb.h"
#include "color.h"

uint8_t *color_hex_to_rgb(uint32_t h)
{
	rgb[0] = RED_FROM_HEX(h);
	rgb[1] = GREEN_FROM_HEX(h);
	rgb[2] = BLUE_FROM_HEX(h);
	return rgb;
}

uint32_t color_rgb_to_hex(uint8_t r, uint8_t g, uint8_t b)
{
	return RGB_TO_HEX(r, g, b);
}