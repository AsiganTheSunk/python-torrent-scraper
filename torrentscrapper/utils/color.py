#!/usr/bin/python
#-*- coding. utf-8 -*-

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[34m'
CYAN = '\033[96m'
BOLD = '\033[1m'
END = '\033[0m'

def red (msg):
	return (RED+BOLD+msg+END)

def blue (msg):
	return (BLUE+BOLD+msg+END)

def green (msg):
	return (GREEN+BOLD+msg+END)

def cyan (msg):
	return (CYAN+BOLD+msg+END)
