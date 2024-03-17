CC = clang
CFLAGS = -Wall -std=c99 -pedantic -g 
LIBS=-lm

# export LD_LIBRARY_PATH=`pwd`
# ssh -L 52151:localhost:52151 dxiao@linux.socs.uoguelph.ca
all: clean libphylib.so _phylib.so

libphylib.so: phylib.o
	$(CC) $(CFLAGS) phylib.o -shared -o libphylib.so $(LIBS)

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

phylib_wrap.c: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

clean:  
	rm -f *.o *.so *.out *.svg phylib.py phylib_wrap.c
