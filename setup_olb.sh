#!/bin/bash
# script to setup and make openlb (set to current version of olb
if [ ! -d olb-1.1r0 ]; then
  wget http://www.optilb.com/openlb/wp-content/uploads/2017/04/olb-1.1r0.tgz
  tar xvfz olb-1.1r0.tgz
  rm olb-1.1r0.tgz
fi
cd olb-1.1r0
make
cd ../cylinder2d
make


