#
#
RM = D:\MinGW\git\usr\bin\rm.exe
MV = D:\MinGW\git\usr\bin\mv.exe
SRCDIR = src
MODULES = mouse color

.PHONY: all clean

all: 
	$(MAKE) -C $(SRCDIR)
	-$(MV) $(SRCDIR)/*.dll .

clean:
	-$(RM) *.dll *.so *.o
	$(MAKE) -C $(SRCDIR) clean