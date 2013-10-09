#!/bin/bash

# -----------------------------------------------------------------------------
# Author: Ole Weidner (ole.weidner@icloud.com)
# Copyright 2013, Ole Weidner
# License under the MIT License
#
# This script launches a rhythmos compute / data resource agent. 
# The launch steps are as follows:
#
# (1) x
# (2) y
# (3) z

# -----------------------------------------------------------------------------
# global variables
#
REMOTE=
OTPTOKEN=
WORKDIR=`pwd`
PYTHON=`which python`

# -----------------------------------------------------------------------------
# print out script usage help
#
usage()
{
cat << EOF
usage: $0 options

This script launches a rhythmos resource agent.

OPTIONS:
   -r      Address and port of the coordination service host
   -t      One-time-password (OTP) authentication token
   -d      The working (base) directory for the agent
           (default is '.')
   -p      The Python interpreter to use, e.g., python2.6
           (default is '/usr/bin/python')
   -h      Show this message

EOF
}

# -----------------------------------------------------------------------------
# create to working directory structure
#
makeworkdir()
{
R_BASE_DIR=$WORKDIR/.rhythmos/
if [ ! -d $R_BASE_DIR ] 
then
    echo "`date +"%m-%d-%Y %T"` - [run-rhythmos-agent.sh] (INFO) - Creating base directory: $R_BASE_DIR"
    mkdir -p $R_BASE_DIR
fi
}

# -----------------------------------------------------------------------------
# bootstrap virtualenv - we always use the latest version from GitHub
#
installvenv()
{
R_SYS_DIR=$WORKDIR/.rhythmos/sys/
# remove any old versionsion
if [ -d $R_SYS_DIR ] 
then
    echo "`date +"%m-%d-%Y %T"` - [run-rhythmos-agent.sh] (INFO) - Removing previous virtualenv: $R_SYS_DIR"
    rm -r $R_SYS_DIR
fi
# create a fresh virtualenv
echo "`date +"%m-%d-%Y %T"` - [run-rhythmos-agent.sh] (INFO) - Bootstraping a fresh virtualenv from https://raw.github.com/pypa/virtualenv"
curl --insecure -s https://raw.github.com/pypa/virtualenv/master/virtualenv.py | $PYTHON - --python=$PYTHON $R_SYS_DIR
source $R_SYS_DIR/bin/activate
echo "`date +"%m-%d-%Y %T"` - [run-rhythmos-agent.sh] (INFO) - Installing Python packages: saga-python, requests"
pip install saga-python requests
}

# -----------------------------------------------------------------------------
# launch the rhythmos agent 
#
launchagent()
{
echo "`date +"%m-%d-%Y %T"` - [run-rhythmos-agent.sh] (INFO) - Starting rhythmos-agent.py..."
python ./rhythmos-agent.py -r $REMOTE -t OTPTOKEN
}

# -----------------------------------------------------------------------------
# MAIN 
#
# parse command line arguments
while getopts “hr:t:d:p” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         r)
             REMOTE=$OPTARG
             ;;
         t)
             OTPTOKEN=$OPTARG
             ;;
         d)
             WORKDIR=$OPTARG
             ;;
         p)
             PYTHON=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $REMOTE ]] || [[ -z $OTPTOKEN ]]
then
     usage
     exit 1
fi

echo "`date +"%m-%d-%Y %T"` - [run-rhythmos-agent.sh] (INFO) - Starting RHYTHMOS environment setup."
# create working direcotries
makeworkdir
# bootstrap virtualenv
installvenv
echo "`date +"%m-%d-%Y %T"` - [run-rhythmos-agent.sh] (INFO) - Completed RHYTHMOS environment setup. "
launchagent

