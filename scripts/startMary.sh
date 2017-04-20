#!/bin/bash

# Change the path settings if your git clone from MaryTTS is in a different path!
MARYTTS_INSTALL_PATH=~/software/git/marytts-installer/

cd $MARYTTS_INSTALL_PATH
./marytts > /dev/null 2>&1 &
cd -