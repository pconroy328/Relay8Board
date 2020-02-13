#!/bin/bash
sudo cp relay8board.service /etc/systemd/system/.
sudo chmod 644 /etc/systemd/system/relay8board.service
sudo systemctl daemon-reload
sudo systemctl start relay8board
sudo systemctl status relay8board
sudo systemctl enable relay8board

