#!/usr/bin/env bash

# Description:
#   The installer for the Saturn service
#
# Usage:
#   Run in the git directory that this file originates from.
#   e.g.
#       $./install.sh
#

function write {
    echo $1 >> $runner
}

# $1 -- location of file to download
# $2 -- Local dest, where to store file
# $3 -- descriptor of what file is (in case of problem with downloading)
function download {
    filename=$(echo $1 | sed 's:.*\/::g')
    dest_file=${2}/${filename}
    if [ -e $dest_file ]; then
        echo "${3} already downloaded at ${dest_file}"
    else
        cd $2 1>/dev/null
        wget $1
        cd - 1>/dev/null
    fi
}


# Make the file that runs the application
runner=~/start_saturn.sh
rm $runner 2>/dev/null
touch $runner
write '#!/bin/bash'
write ''
write "python ${PWD}/saturn/saturn.py"
write ''
chmod +x $runner

# Make the SaturnServer directory tree
mkdir ~/SaturnServer 2>/dev/null
mkdir ~/SaturnServer/test_resources 2>/dev/null
mkdir ~/SaturnServer/images 2>/dev/null

# Download the files needed to run and test the server
download 'http://degas.ecs.soton.ac.uk/~productizer/test_resources/test_tile.jpg' ~/SaturnServer/test_resources 'test_tile.jpg'
download 'http://seurat.ecs.soton.ac.uk/~productizer/Googlenet_791113_192patch.prm' ~/SaturnServer 'prm file'

# Ensure that the prm file is downloaded!
if [ -e ~/SaturnServer/Googlenet_791113_192patch.prm ] ; then
    echo -e "\e[32m-- Saturn Fully Installed --\e[39m"
else
    echo -e "\e[31m-- Saturn Installation FAILED --\e[39m"
fi