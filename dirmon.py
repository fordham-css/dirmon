# dirmon
# primitive directory monitoring
#
# USAGE
# Just navigate to the directory you want to track then run the command:
# > python dirmon.py
#
# REQUIREMENTS
# This program requires a bash_history merge across tty sessions.
# > export HISTCONTROL=ignoredups:erasedups  
# > shopt -s histappend
# > export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"
#
# TO DAEMONIZE THIS SCRIPT
# use command:
# > python dirmon.py &
# NOTE: you should disable all "print" commands in the daemon script in the "difference_hunter" module


import time
import psutil
import os
import re
import easygui

cur_dir_path = os.getcwd()

splitter = re.compile(r'/')
cur_dir = splitter.split(cur_dir_path)
cur_dir = '/' + cur_dir[len(cur_dir)-1]
splitter = re.compile(r'\n')
count = 0

home = os.path.expanduser('~')

do_loc = cur_dir_path + '/.dirmon_origin'
d_loc = cur_dir_path + '/.dirmon'

if not os.path.exists(do_loc):
    open(do_loc, 'w').close()
if not os.path.exists(d_loc):
    open(d_loc, 'w').close()

print '\n============================================================'
print 'dirmon initiated!\nLogs kept at ./.dirmon and ./.dirmon_origin'
print 'Initiating tracker for current directory:'+cur_dir
print 'At path:' + cur_dir_path
print '============================================================'

def prime_logger():
    bash_history_raw = open(home+'/.bash_history', 'r')
    bash_history_text = bash_history_raw.read()
    with open(cur_dir_path + '/.dirmon_origin','w') as f:
        f.write(bash_history_text)
        f.close()

def bash_history():
    # import bash history
    bash_history_raw = open(home +'/.bash_history', 'r')
    bash_history_text = bash_history_raw.read()
    bash_history_array = splitter.split(bash_history_text)
    return bash_history_array
    
def dirmon_origin():
    # open dirmon  origin file
    dirmon_origin_raw = open(cur_dir_path + '/.dirmon_origin','r+w')
    dirmon_origin_text = dirmon_origin_raw.read()
    dirmon_origin_array = splitter.split(dirmon_origin_text)
    return dirmon_origin_array

def difference_scan(x,y):
    # Tally counts in x
    seen_count = {}
    differences = 0
    for i in x:
        if i not in seen_count:
            # First time seeing this number.
            seen_count[i] = 1
        else:
            # Number has been seen.
            seen_count[i] += 1

    for j in y:
        if j not in seen_count:
            seen_count[j] = 1
        elif seen_count[j] > 1:
            seen_count[j] -= 1
        else:
        	seen_count[j] += 1
    
    for k in seen_count:
        if (k in x and k not in y) or (k in y and k not in x):
            while seen_count[k] > 0:
                seen_count[k] -= 1
        elif seen_count[k] == 1:
            seen_count[j] += 1
            differences += 1
    return differences
       
def difference_array(x,y):
    # Tally counts in x
    seen_count = {}
    results = []
    
    for i in x:
        if i not in seen_count:
            # First time seeing this number.
            seen_count[i] = 1
        else:
            # Number has been seen.
            seen_count[i] += 1
    
    for j in y:
        if j not in seen_count:
            seen_count[j] = 1
        elif seen_count[j] > 1:
            seen_count[j] -= 1
        else:
        	seen_count[j] += 1
    
    for k in seen_count:
        if (k in x and k not in y) or (k in y and k not in x):
            while seen_count[k] > 0:
                results.append(k)
                seen_count[k] -= 1
        elif seen_count[k] == 1:
            results.append(k)
    return results

def difference_hunter(count):
    flag = difference_scan(dirmon_origin(),bash_history())
    # '[' + str(count) + ']' + ' ' + 'Tracking changes in ' + cur_dir_path + ':' + str(flag)
    if flag!=0 and flag>0:
        dirmon_array = difference_array(dirmon_origin(),bash_history())
        dirmon = ''
        for f in dirmon_array:
            dirmon = dirmon + '\n' + f
        with open(cur_dir_path + '/.dirmon','w') as f:
            f.write(dirmon)
            f.close
    return flag
    
def dir_intrusion(current_directory,dirmon):
    results = []
    for each in dirmon:
        if current_directory not in each:
            print 'dirmon: Possible threat detected with command:' + each
            results.append(each)
        else:
            print 'dirmon: Unlikely threat Detected with command:' + each
    return results

def run():
    prime_logger()
    count = 0
    flag_log =0
    while True:
        flag = difference_hunter(count)
        if flag!=flag_log and flag>flag_log:
            with open(cur_dir_path + '/.dirmon','r+w') as f:
                df = f.read()
                dirmon = splitter.split(df)
                intrusions = dir_intrusion(cur_dir,dirmon)
            	easygui.msgbox('Found '+str(len(intrusions))+' intrusions into '+cur_dir+'\n'+str(intrusions), title='dirmon')
                flag_log=flag
        time.sleep(.5)
        count += 1
		
if __name__ == "__main__":
    run()