#!/bin/sh
service ppbed start
service ppbwd start
tail -F /dev/null
