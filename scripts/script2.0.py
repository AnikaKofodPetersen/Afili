
#import packages and change directory
import os
os.chdir('{}/blast_folder'.format(scripts))										
file_count = 0
import io 
from contextlib import redirect_stdout 
text_trap = io.StringIO()


#Move database to proper PATH
os.system("cp ../../db/"+str(genus)+"/* .")


for ffn_file in os.listdir():								#iterate over all files in directory
	if ffn_file.endswith(".ffn"):							#specifies .ffn files
		file_count += 1
		
		with open("../../db/"+str(genus)+"/database_names.txt",'r') as databases:	#for all individual genomes
			for line in databases:
				command = "blastn -query " + str(ffn_file)+" -db " + str(line[:-1]) +" -outfmt 6 -perc_identity "+ str(identity)+" -qcov_hsp_perc "+str(coverage)
				command += "> " + str(ffn_file) + "vs"+str(line[:-1])+"_blast"
				with redirect_stdout(text_trap):
					os.system(command)						#perform a blast search 
					
				print("BLAST: query " + str(ffn_file) + " database " +str(line))		#screen output 

#Make ending indicator
os.chdir('..')
os.system("touch blast_done")

