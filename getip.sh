#!/bin/sh
#This will return the local IP adress(es) and filters those that aren't usefull (127.0.0.1, 10.X.X.X, etc)
ifconfig | grep -E -o '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' | tail -n 2 | head -n 1
