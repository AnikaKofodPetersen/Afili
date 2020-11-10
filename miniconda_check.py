#!/usr/bin/env python3
#import necessary packages
import os
import sys
import subprocess



try:
	#Check if miniconda is installed
	output = subprocess.check_output(['conda','--version'])
	if output.decode("utf-8").startswith("Command"):
		raise FileNotFoundError
		#Download miniconda
except FileNotFoundError as error:
	print("##################################################################\n\n\n")
	print("To succesfully use Afili you must have conda. Please install Anaconda or Miniconda before use.")
	print("\n\n\n##################################################################")
	sys.exit(1)
 