#!/usr/bin/python

# Copyright (C) 2013 Maria Christopoulou
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#    RTTY Transmitter- ITA2 Code
#    
#    This Python script transmits a message, using the RTTY mode.
#    
#    Issues:
#    1. Change all values of the dictionary to MSB on the right	
#    2. Play the .wav files using Python and not calling the Bash	
#    3. The transmission isn't continuous and the message isn't 
#       received correctly. A different approach has to be followed here.
#    4. Add look up table for Baudot Figures
# 			    
# 
#    I run the code on BeagleBone Black (BBB), to use it as a Software Defined Radio.
#    The command "aplay -L" lists my Usb Audio Dongle as "Dongle".
#    Run this command to see if a different name is used on your BBB.
#
#    References:
#    en.wikipedia.org/wiki/Baudot_code
#
################################################################################


from array import array
import subprocess

##################################################################
# ITA2 Look Up Table						 
# MSB on Right							  
# TODO : Correct All values					  
# for MSB on right 						 
##################################################################

baudot = {'Q':[1,1,1,0,1], 'W':[1,0,0,1,1], 'E':[1,0,0,0,0],
		'R':[0,1,0,1,0], 'T':[1,0,0,0,0], 'Y':[1,0,1,0,1],
		'U':[0,0,1,1,1], 'I':[0,0,1,1,0], 'O':[1,1,0,0,0], 
		'P':[0,1,1,0,1], 'A':[0,0,0,1,1], 'S':[1,0,1,0,0], 
		'D':[1,0,0,1,0], 'F':[0,1,1,0,1], 'G':[1,1,0,1,0], 
		'H':[1,0,1,0,0], 'J':[0,1,0,1,1], 'K':[0,1,1,1,1], 
		'L':[0,1,0,0,1], 'Z':[1,0,0,0,1], 'X':[1,1,1,0,1], 
		'C':[0,1,1,1,0], 'V':[0,1,1,1,1], 'B':[1,1,0,0,1], 
		'N':[0,1,1,0,0], 'M':[1,1,1,0,0]}

space = [0,0,1,0,0]

# Message to be sent

message="CQ CQ CQ DE SVPLE"


# Loop through message string and
# match letters from Baudot dict
	
subprocess.call(["aplay","-D","default:CARD=Dongle","wait_state.wav"])

for k in message:
	
	# Recognize white spaces
	if ord(k) == 32:
		a = space
	else:
		a = baudot.setdefault(k)
	
	b = len(a)
	
	# Start Bit
	subprocess.call(["aplay","-D","default:CARD=Dongle","space.wav"])

	for i in a:
		if i==1:
			subprocess.call(["aplay","-D","default:CARD=Dongle","mark.wav"])
		elif i==0:
			subprocess.call(["aplay","-D","default:CARD=Dongle","space.wav"])
		else:
			break;
					
		subprocess.call(["aplay","-D","default:CARD=Dongle","stop_bit.wav"])


