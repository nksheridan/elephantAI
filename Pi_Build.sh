#!/bin/bash
# script to build protobuf and tensorflow on raspberry pi

echo "Script to build protobuf and tensforlow for Raspberry Pi"
cd /home/pi/tensorflow/tensorflow/contrib/makefile/downloads/protobuf
pwd
echo "configurations.."
sudo ./autogen.sh
./configure
clear
echo "make protobuf"
make
clear
echo "make install protobuf"
sudo make install
sudo ldconfig
cd /home/pi/tensorflow
echo "export HOST_NSYNC_LIB=`tensorflow/contrib/makefile/compile_nsync.sh`"
sudo export HOST_NSYNC_LIB=`tensorflow/contrib/makefile/compile_nsync.sh`
echo "export TARGET_NSYNC_LIB=$HOST_NSYNC_LIB"
sudo export TARGET_NSYNC_LIB="$HOST_NSYNC_LIB"
clear
echo "Build TensforFlow now.."
sudo make -f tensorflow/contrib/makefile/Makefile HOST_OS=PI TARGET=PI \ OPTFLAGS="-Os -mfpu=neon-vfpv4 -funsafe-math-optimizations -ftree-vectorize" CXX=g++-4.8

