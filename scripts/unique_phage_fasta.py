#!/usr/bin/env python3

#import packages and change directory
import os
import re
os.chdir("blast_folder")

names = dict()						
phage_dict = dict()
check_dict = dict()
with open("../host_fastas/name_storage.txt", 'r') as name_storage:						#Collect name of hosts and prophage position
	for line in name_storage:
		names[line.split()[1]]= line.split()[0]

		
with open("unique_blastdict", 'r') as u_blastdict:						#For each unique prophage, collect hostname, start position and end position
	line_count = 0
	for line in u_blastdict:
		line_count += 1
		accession = line.split()[0]
		accession = accession.split("_phage_")[1]
		number = int(names[accession]) 
		start = int(line.split()[1]) -1 
		end = int(line.split()[2]) -1
		
		

		with open("../host_fastas/unique_fasta" + str(number) + ".fna", 'r') as genome_fasta:			#Collect prophages from the host fasta file
			prophage = []
			print("Collecting prophage from  " +str(genome_fasta.readline()))
			for seq_line in genome_fasta:												#Save all amino acids 
				for char in seq_line:
					prophage += [char]
			prophage = [i for i in prophage if i != '\n']								#Delete newline characters
			if start < end:																#'pick out' prophage from host 
					prophage = prophage[start+1:end+1]
			elif end < start:
					prophage = prophage[end+1:start+1]
			prophage_string = "".join(prophage)
			if line.split()[0] not in check_dict:										#If more than one prophage is found in the same host, numerate them 
				check_dict[line.split()[0]] = 1
			else:
				check_dict[line.split()[0]]+= 1
			phage_dict[line.split()[0] + "_" + str(check_dict[line.split()[0]])] = prophage_string

#Make/change directory 
os.mkdir("../collected_phages")
os.chdir("../collected_phages")


for item in phage_dict.items():														#Write the prophage fasta file
	with open(str(item[0]) + ".fna", 'a') as outfile:
		outfile.write(">" + str(item[0]) + " prophage collected \n" + str(item[1]) + "\n")

os.chdir("..")

for original_fasta in os.listdir():													#Write a file with the names of the original ppBGCs without illegal characters
	if original_fasta.endswith(".fna"):
		with open(original_fasta, 'r') as fasta_file:
			header = fasta_file.readline()[1:]
			header = re.sub(r'[^\d*\w*_*\.*]', "_", header, count=0)
			with open("original_names.txt" ,'a') as original_names:
				original_names.write(header + "\n")

																					#Make copies of the original ppBGCs with more appropriate names for phylogenetic display
			command = "cp " + str(original_fasta) + " collected_phages/" + str(header) + ".fna"
		os.system(command)
		print("collecting original prophage " + str(header))

#Collect all phages in a single file aswell
os.chdir("collected_phages")
os.system("cat *.fna >> collected_all")
os.chdir("..")

#Make ending indicator
os.system("touch collected_phages_done")
