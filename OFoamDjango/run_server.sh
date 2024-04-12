#!/bin/bash

./run_display.sh

source /opt/openfoam7/etc/bashrc

# git clone https://github.com/Franjcf/hybridPorousInterFoam.git
cd hybridPorousInterFoam/OpenFoamV7/
./Allwclean
./Allwmake
cd ../../
python3 manage.py runserver 0.0.0.0:8000
