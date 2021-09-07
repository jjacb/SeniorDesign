#!/bin/bash

#Txt file containing names of all the images
LIST=list.txt
#Number of horizontal squares(int > 0)
NX=6
#Number of vertical squares(int > 0)
NY=9
#Square size in cm
SQSIZE=2.5

./stereo_calibrate $LIST $NX $NY $SQSIZE 
