#import packages and move fasta files
import os
import sys


#Perform a gene prediction on all fasta files with PROKKA 
file_count = 0
for ppBGC_file in os.listdir():
	if ppBGC_file.endswith(".fna"):
		file_count += 1
		command = "prokka --kingdom Viruses --quiet --prefix {} --outdir prokka_{} {}".format(file_count, str(file_count), ppBGC_file)
		print( "Performing a gene prediction on {}".format(ppBGC_file))
		os.system(command)
