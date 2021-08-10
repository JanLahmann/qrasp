#!/bin/bash
sleep 15
/usr/bin/python3 /home/pi/qrasp/qrasp.py 

# enable in crontab with
# sudo crontab -e
# @reboot sudo -u pi -H -- sh -c /home/pi/qrasp/qrasp.sh > /home/pi/qrasp/qrasp.sh.log 2>&1
