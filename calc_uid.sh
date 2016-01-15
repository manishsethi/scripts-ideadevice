#!/bin/bash
##############################################################################
# Given a file of the form (you can use /etc/passwd):

# root:x:0:0:root:/root:/bin/bash
# daemon:x:1:1:daemon:/usr/sbin:/bin/sh
# bin:x:2:2:bin:/bin:/bin/sh
# sys:x:3:3:sys:/dev:/bin/sh
# sync:x:4:65534:sync:/bin:/bin/sync
# games:x:5:60:games:/usr/games:/bin/sh
# man:x:6:12:man:/var/cache/man:/bin/sh
# lp:x:7:7:lp:/var/spool/lpd:/bin/sh
# mail:x:8:8:mail:/var/mail:/bin/sh
# news:x:9:9:news:/var/spool/news:/bin/sh
# Write a bash 4.0 shell script to sum the third field, delimited by ':'.
# Your script should take the filename to process as the first command line argument.
# The prohibition on external commands means that you do not have access 
# to commands like sed, grep, awk, cut and so on.

# Author: Manish Sethi
# Date: 15-1-2016
###############################################################################

FILE=$1

sum=0

while IFS=: read user pass uid gid full home shell          
do          
  sum=$((sum + uid))
done <$FILE

#Print the value
echo "The sum of the third field(UID) is: $sum"
