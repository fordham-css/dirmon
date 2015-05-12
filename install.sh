#!/bin/bash
echo ' '
echo 'Installing dirmon...'

# install merged bash history requirements
echo 'Merging bash histories...'
export HISTCONTROL=ignoredups:erasedups
shopt -s histappend
export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"

# move dirmony.py
echo 'Moving to python library...'
sudo cp dirmon.py /Library/Python/2.7/site-packages/dirmon.py

# create command
echo 'Creating command...'
echo 'sudo python /Library/Python/2.7/site-packages/dirmon.py &' > init
sudo cp init /usr/bin/dirmon
chmod +x /usr/bin/dirmon

echo 'dirmon successfully installed!'
echo ' ʕ•ᴥ•ʔ < "happy monitoring!"'