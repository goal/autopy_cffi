#pragma once
#ifndef COLOR_H
#define COLOR_H

static uint8_t rgb[3];

uint8_t *color_hex_to_rgb(uint32_t h);

uint32_t color_rgb_to_hex(uint8_t r, uint8_t g, uint8_t b);

#endif