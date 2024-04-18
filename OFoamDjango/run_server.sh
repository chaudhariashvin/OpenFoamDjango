#!/bin/bash
set -x

./run_display.sh

source /opt/openfoam7/etc/bashrc
export PATH="/home/foam/OpenFOAM/-7/platforms/linux64GccDPInt32Opt/bin/":$PATH
export LD_LIBRARY_PATH="/home/foam/OpenFOAM/-7/platforms/linux64GccDPInt32Opt/lib":$LD_LIBRARY_PATH
# export PYTHONPATH=/home/foam/.local/lib/python3.8/site-packages

whoami
echo $USER

ls -l
#  git clone https://github.com/Franjcf/hybridPorousInterFoam.git
# ls -l hybridPorousInterFoam
# cd hybridPorousInterFoam/OpenFoamV7/
# ./Allwclean
# ./Allwmake
# cd ../../
# pip3 freeze
# which python3
# python3 -m site
export MPLCONFIGDIR="./.config/matplotlib"
python3 manage.py runserver 0.0.0.0:8000

set +x