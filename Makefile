#
#

SRCDIR = src
MODULES = mouse color

.PHONY: all clean

all: 
	cd $(SRCDIR) && make
	-mv $(SRCDIR)/*.dll .

clean:
	-rm *.dll *.so *.o
	cd $(SRCDIR) && make clean