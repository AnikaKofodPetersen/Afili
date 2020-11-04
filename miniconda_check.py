#!/usr/bin/env python3
#import necessary packages
import os
import sys
import subprocess
import re


try:
	#Check if miniconda is installed
	output = subprocess.check_output(['conda','--version'])
	if output.decode("utf-8").startswith("Command"):
		raise FileNotFoundError
		#Download miniconda
except FileNotFoundError as error:
	os.system("wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh")
	os.system("bash Miniconda3-latest-Linux-x86_64.sh")
	print("##################################################################\n\n\n")
	print("To succesfully install Miniconda, you should restart your terminal and set PATH to miniconda as follows:\n$ export PATH=/path/to/miniconda3/bin_$PATH\n")
	print("\n\n\n##################################################################")
	sys.exit()
print("Miniconda is available") 