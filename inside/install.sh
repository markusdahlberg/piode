#!/bin/bash
# Setup Script for Project Piode Receiver

if [ $(id -u) -eq 0 ]; then
	cp /src/* /usr/piode/
	cp /conf/* /etc/piode/
	cp /systemd/piode-send.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable service piode-receive
	systemctl start service piode-receive
else
        echo "Setup failed due to lack of root privileges!"
        exit 1
fi