#!/bin/bash

PID=`ps -ef | grep marytts | grep -v grep  | awk '{print $2}'`

if [[ "" != "$PID" ]]; then
    echo "Kill process $PID"
    kill -9 $PID
fi