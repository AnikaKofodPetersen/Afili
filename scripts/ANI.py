#!/usr/bin/env python3

#import packages
import os
import io 
from contextlib import redirect_stdout 
text_trap = io.StringIO()

#Change names of files to include ST 
os.chdir("ANI")
with open("../newick_trees/SpeciesMetadata.txt",'r') as species:
	query = []
	for line in species:
		name = line.split("\t")[0]
		ST = line.split("\t")[1][:-1]
		query += ["./"+str(name)+str(ST)+".fna"]
		for fasta in os.listdir():
			if fasta[:-4] == name:
				command = "mv " + str(fasta) + " " + str(name)+str(ST) +".fna"
				os.system(command)
			elif fasta[:-5] == name:
				command = "mv " + str(fasta) + " " + str(name)+str(ST) +".fna"
				os.system(command)

#Make query list
query.pop(0)
with open("query_list.txt","a") as query_list:
	for entry in query:
		query_list.write(entry + "\n")		

#Perform an ANI analysis
print("Performing an ANI analysis (average nucleotide identity). This might take a while.")
os.system("fastANI --ql query_list.txt --rl query_list.txt --matrix -o ANI_output  > /dev/null 2>&1")


#change directory and format output
os.chdir("..")


