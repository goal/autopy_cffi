#
#

SRCDIR = src
MODULES = mouse color

.PHONY: all clean

all: 
	$(MAKE) -C $(SRCDIR)
	-mv $(SRCDIR)/*.dll .

clean:
	-rm *.dll *.so *.o
	$(MAKE) -C $(SRCDIR) clean