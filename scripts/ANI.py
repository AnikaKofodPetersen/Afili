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
			if fasta.endswith(".fna") and fasta.startswith(name):
				command = "mv " + str(fasta) + " " + str(name)+str(ST) +".fna"
				os.system(command)


#Make query list
query.pop(0)
count = 0
with open("query_list.txt","a") as query_list:
	for entry in query:
		count += 1
		query_list.write(entry + "\n")		

#Perform an ANI analysis
print("Performing an ANI analysis (average nucleotide identity). This might take a while.")
try:
	os.system("fastANI --ql query_list.txt --rl query_list.txt --matrix -o ANI_output --fragLen 1500 --minFraction 0.1")
except Exception as error:
	print(error)
if not "ANI_output.matrix" in os.listdir():
	print("##############################################################")
	print("ERROR MESSAGE: A correct ANI heat map was not produced. \n Possible reason: Identity < 80%")
	print("##############################################################")
	nul_matrix =[str(count)]
	count = -1
	with open("query_list.txt","r") as query_list:
    		for line in query_list:
        		count += 1
        		add = line[:-1]
        		add += ("\t0"*count)
        		nul_matrix.append(add[:])
	with open("ANI_output.matrix", "a") as nul_file:
    		for line in nul_matrix:
        		nul_file.write(line + "\n")
			

#change directory and format output
os.chdir("..")


