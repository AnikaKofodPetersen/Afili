#import packages and change directory
import os
os.chdir("blast_folder")

unique_lines = set()
with open("accepted_phages.txt",'r') as blastdict:						#Pick the Unique lines in the collected accepted prophages
	for line in blastdict:
		if line not in unique_lines:
			unique_lines.add(line)
			
with open("unique_blastdict", 'a') as unique_blastdict:					#make a new file with the unique accepted prophages
	for lineadd in unique_lines:
		unique_blastdict.write(lineadd)

#Make ending indicator
os.system("touch ../unique_lines_done")
