default: png2raw raw2png

.PHONY: default

png2raw: png2raw.c
	gcc -shared -fPIC -Wall -o $@ $< `pkg-config --libs --cflags libpng`

raw2png: raw2png.c
	gcc -shared -fPIC -Wall -o $@ $< `pkg-config --libs --cflags libpng`

png2raw_main: png2raw.c
	gcc -Wall -o $@ $< `pkg-config --libs --cflags libpng`

raw2terminal := python3 raw2terminal.py
png          := /home/dragorn421/Documents/oot/assets/objects/object_link_boy/eyes_shock.ci8.png

test: png2raw_main
	./png2raw_main $(png) | $(raw2terminal)
	./png2raw_main --rgba32 $(png) | $(raw2terminal)
	./png2raw_main --palette-rgba32 $(png) | $(raw2terminal)
	./png2raw_main --palette-indices $(png) | $(raw2terminal)
	./png2raw_main --palette-indices $(png) | $(raw2terminal) --format=i8
	./png2raw_main --dimensions $(png)
