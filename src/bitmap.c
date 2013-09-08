#include "bitmap_find.h"
#include "color_find.h"
#include "screen.h"
#include "io.h"
#include "pasteboard.h"
#include "str_io.h"
#include <assert.h>
#include <stdio.h>


void bitmap_dealloc(MMBitmapRef bitmap)
{
	if (bitmap != NULL) {
		destroyMMBitmap(bitmap);
		bitmap = NULL;
	}
}

static bool parseImageIOArgs(const char *path, const char *format, MMImageType *type)
{
	int pathLen = strlen(path);

	assert(path != NULL);
	assert(type != NULL);

	if (format == NULL) {
		const char *ext = getExtension(path, pathLen);

		if (ext == NULL) {
			return false;
		}

		*type = imageTypeFromExtension(ext);
	} else {
		*type = imageTypeFromExtension(format);
	}

	if (*type == kInvalidImageType) {
		return false;
	}

	return true;
}

/* -- Bitmap class method definitions -- */

MMBitmapRef bitmap_open(const char *path, const char *format)
{
	MMBitmapRef bitmap;
	MMImageType type;

	MMIOError err;

	if (!(parseImageIOArgs(path, format, &type))) {
		return NULL;
	}

	if ((bitmap = newMMBitmapFromFile(path, type, &err)) == NULL) {
		return NULL;
	}

	return bitmap;
}

MMBitmapRef bitmap_from_string(const char *str)
{
	size_t len = strlen(str);

	MMBitmapRef bitmap;
	MMBMPStringError err;

	if ((bitmap = createMMBitmapFromString(str, len, &err)) == NULL) {
		return NULL;
	}

	return bitmap;
}

/* -- Bitmap instance method definitions -- */

/* Returns false and sets error if |bitmap| is NULL. */
bool bitmap_ready(MMBitmapRef bitmap)
{
	if (bitmap == NULL || bitmap->imageBuffer == NULL) {
		return false;
	}
	return true;
}

// out with size 200 is enough
bool bitmap_str(MMBitmapRef bitmap, char *out)
{
	if (!bitmap_ready(bitmap)) return false;
	sprintf(out, "<Bitmap with resolution %lu%lu, \
	                    %u bits per pixel, and %u bytes per pixel>",
	                    (unsigned long)bitmap->width,
	                    (unsigned long)bitmap->height,
	                    bitmap->bitsPerPixel,
	                    bitmap->bytesPerPixel);

	return true;
}

MMBitmapRef bitmap_deepcopy(MMBitmapRef bitmap)
{
	return bitmap == NULL ? NULL : copyMMBitmap(bitmap);
}

MMBitmapRef bitmap_get_portion(MMBitmapRef bitmap, MMRect rect)
{
	MMBitmapRef portion = NULL;

	if (!MMBitmapRectInBounds(bitmap, rect)) {
		return NULL;
	}

	portion = copyMMBitmapFromPortion(bitmap, rect);

	if (portion == NULL) {
		return NULL;
	}
	return portion;
}

bool bitmap_point_in_bounds(MMBitmapRef bitmap, MMPoint point)
{
	if (!bitmap_ready(bitmap)) {
		return NULL;
	}

	if (MMBitmapPointInBounds(bitmap, point)) {
		return true;
	}

	return false;
}

bool bitmap_copy_to_pboard(MMBitmapRef bitmap)
{
	MMPasteError err;

	if (!bitmap_ready(bitmap)) return false;
	if ((err = copyMMBitmapToPasteboard(bitmap)) != kMMPasteNoError) {
		return false;
	}

	return true;
}

bool bitmap_save(MMBitmapRef bitmap, const char *path, const char *format)
{
	MMImageType type;

	//printf("start check!\n");
	if (!parseImageIOArgs(path, format, &type) || !bitmap_ready(bitmap)) {
		return false;
	}

	printf("start save!!\n");
	printf("path=%s\n", path);
	printf("type=%d\n", type);
	if (saveMMBitmapToFile(bitmap, path, type) != 0) {
		return false;
	}

	return true;
}

bool bitmap_to_string(MMBitmapRef bitmap, char *buf)
{
	MMBMPStringError err;

	if (!bitmap_ready(bitmap)) return false;

	if ((buf = (char *)createStringFromMMBitmap(bitmap, &err)) == NULL) {
		return false;
	}
	return true;
}

// TODO: return value specified
MMRGBHex Bitmap_get_color(MMBitmapRef bitmap, MMPoint point)
{
	if (!bitmap_ready(bitmap)) return 0;

	if (!MMBitmapPointInBounds(bitmap, point)) {
		return 0;
	}

	return MMRGBHexAtPoint(bitmap, point.x, point.y);
}

MMPoint bitmap_find_color(MMBitmapRef bitmap, MMRGBHex color, float tolerance)
{
	MMRect rect = MMBitmapGetBounds(bitmap);
	MMPoint point = {-1, -1};

	if (findColorInRect(bitmap, color, &point, rect, tolerance) == 0) {
		return point;
	}

	return point;
}

// size of list should be larger than sizeof(MMPoint) * count
MMPoint *bitmap_find_every_color(MMBitmapRef bitmap, MMRGBHex color, float tolerance, MMPoint *list)
{
	if (!bitmap_ready(bitmap)) return NULL;
	MMRect rect = MMBitmapGetBounds(bitmap);
	MMPointArrayRef pointArray;

	pointArray = findAllColorInRect(bitmap, color, rect, tolerance);
	if (pointArray == NULL) return NULL;

	memcpy(list, pointArray->array, sizeof(MMPoint) * pointArray->count);
	destroyMMPointArray(pointArray);
	if (list == NULL) return NULL;

	return list;
}

int bitmap_count_of_color(MMBitmapRef bitmap, MMRGBHex color, float tolerance)
{
	if (!bitmap_ready(bitmap)) return 0;
	MMRect rect = MMBitmapGetBounds(bitmap);

	return countOfColorsInRect(bitmap, color, rect, tolerance);
}

MMPoint bitmap_find_bitmap(MMBitmapRef bitmap, MMBitmapRef sbitmap, float tolerance)
{
	MMPoint point = {-1, -1};
	printf("tolenrance=%f\n", tolerance);
	if (!bitmap_ready(bitmap) || !bitmap_ready(sbitmap)) {
		printf("bitmap is not ready yet!\n");
		return point;
	}

	MMRect rect = MMBitmapGetBounds(bitmap);
	printf("x=%d,y=%d,width=%d,height=%d\n", rect.origin.x, rect.origin.y, rect.size.width, rect.size.height);

	if (findBitmapInRect(sbitmap, bitmap, &point,
	                     rect, tolerance) == 0) {
		return point;
	}
	
	return point;
}

MMPoint *bitmap_find_every_bitmap(MMBitmapRef bitmap, MMBitmapRef sbitmap, float tolerance, MMPoint *list)
{
	if (!bitmap_ready(bitmap) || !bitmap_ready(sbitmap)) return NULL;

	MMPoint point;
	MMPointArrayRef pointArray;
	MMRect rect = MMBitmapGetBounds(bitmap);

	if (findBitmapInRect(bitmap, sbitmap, &point,
	                     rect, tolerance) == 0) {
		return NULL;
	}

	pointArray = findAllBitmapInRect(bitmap, sbitmap, rect, tolerance);
	if (pointArray == NULL) return NULL;

	memcpy(list, pointArray->array, sizeof(MMPoint) * pointArray->count);
	destroyMMPointArray(pointArray);

	return list;
}

int bitmap_count_of_bitmap(MMBitmapRef bitmap, MMBitmapRef sbitmap, float tolerance)
{
	if (!bitmap_ready(bitmap) || !bitmap_ready(sbitmap)) return 0;

	MMRect rect = MMBitmapGetBounds(bitmap);

	return countOfBitmapInRect(bitmap, sbitmap, rect, tolerance);
}
