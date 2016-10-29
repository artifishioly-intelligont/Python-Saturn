#!/usr/bin/env bash

# Description:
#   The installer for the Saturn service
#
# Usage:
#   Run in the git directory that this file originates from.
#   e.g.
#       $./install.sh
#

# Make the file that runs the application
runner=~/start_saturn.sh
rm $runner && true
touch $runner

function write {
    echo $1 >> $runner
}

write '#!/bin/bash'
write ''
write "python ${PWD}/saturn/saturn.py"
write ''
chmod +x $runner

mkdir ~/SaturnServer && true
cd ~/SaturnServer
wget http://seurat.ecs.soton.ac.uk/~productizer/Googlenet_791113_192patch.prm

mkdir ~/SaturnServer/images && true

