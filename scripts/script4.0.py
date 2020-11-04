
#import packages and change directory
import os
fasta_count = 0
id_set = set()
import io 
from contextlib import redirect_stdout 
text_trap = io.StringIO()
				
os.chdir("blast_folder")		

with open("accepted_phages.txt", 'r') as accepted_blastdict:		#Collect all unique ID's
	for line in accepted_blastdict:
		entry_id = line.split("_phage_")[1]
		entry_id = entry_id.split()[0]
		if entry_id not in id_set:
			id_set.add(entry_id)
			
os.mkdir("../host_fastas")
os.system("mv " + str(database_name) + "* ../host_fastas")			#Move the collected database to search path
os.chdir("../host_fastas")

for id_entry in id_set:
			
	print( "Getting database entry for: " + id_entry)				#Collect the fasta files for the genomes from the database
	fasta_count += 1
	with open("name_storage.txt", 'a') as name_storage:
		name_storage.write(str(fasta_count) + "\t" + str(id_entry) + "\n")	#Name it properly
			
																			#Collect the database host entry
	command = "blastdbcmd -entry " + str(id_entry) + " -db "+str(database_name) +" -out unique_fasta" + str(fasta_count) + ".fna"
	with redirect_stdout(text_trap):
		os.system(command)
				
#Make ending indicator
os.system("touch ../collection_host_done")
