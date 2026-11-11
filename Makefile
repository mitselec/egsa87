CC ?= cc
CFLAGS ?= -O2 -Wall -std=c99
BIN = build/egsa87_test

.PHONY: all build test-c test clean

all: build

build: $(BIN)

$(BIN): C/egsa87.c C/egsa87_test.c C/egsa87.h
	mkdir -p build
	$(CC) $(CFLAGS) -o $@ C/egsa87.c C/egsa87_test.c -lm

test-c: $(BIN)
	./$(BIN)

test: test-c
	pytest -q

clean:
	rm -rf build
