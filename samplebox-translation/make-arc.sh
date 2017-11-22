#!/usr/bin/env bash

foldername=`echo $(pwd) | awk -F "/" '{ print $NF }'`
today=`date "+%Y%m%d"`
git archive HEAD --format=zip --worktree-attributes -o ../${foldername}-${today}-head.zip
