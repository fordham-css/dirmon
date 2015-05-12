#!/bin/bash
echo ' '
echo 'Uninstalling dirmon...'

# delete dirmony.py
echo 'Deleting dirmon.py in python library...'
sudo rm /Library/Python/2.7/site-packages/dirmon.py

# delete init
sudo rm ./init

# delete command
sudo rm /usr/bin/dirmon

echo 'dirmon successfully uninstalled!'
echo ' ʕ•ᴥ•ʔ < "Thanks!"'