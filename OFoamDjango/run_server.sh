#!/bin/bash
set -x

./run_display.sh

source /opt/openfoam7/etc/bashrc

whoami
echo $USER

ls -l
#  git clone https://github.com/Franjcf/hybridPorousInterFoam.git
# ls -l hybridPorousInterFoam
# cd hybridPorousInterFoam/OpenFoamV7/
# ./Allwclean
# ./Allwmake
# cd ../../
pip3 freeze
which python

python3 manage.py runserver 0.0.0.0:8000

set +x