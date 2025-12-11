#!/bin/sh
mkdir -p bin
clang -Oz -g0 -flto=full daemon.c -o bin/gamepadifyd
strip -s --remove-section=.comment bin/gamepadifyd
