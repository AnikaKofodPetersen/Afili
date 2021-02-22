#import necessary packages
import os
import sys
import subprocess
import re

#Default setting
typestrain = False
coverage = 70
identity = 70 
max_thres_set = 150
min_thres_set = 50
min_genes_set = 60
gap_thres_set = 15
curdir = str(os.getcwd())
cores = subprocess.check_output(['nproc']).decode("utf-8")


#Define script path
scripts = sys.argv[0]
scripts = "/".join(scripts.split("/")[:-1])

#Define user command line input in scripts
arguments = sys.argv[1:]
for argument in range(0,len(arguments)):
	#Fasta files(s)
	if arguments[argument].startswith("-F") or arguments[argument].startswith("--fasta"):
		fasta_folder = curdir +"/"+arguments[argument+1]
		output_folder = fasta_folder
	#Output directory
	if arguments[argument].startswith("-O") or arguments[argument].startswith("--output"):
		output_folder = curdir +"/"+arguments[argument+1]
		if os.path.isdir(output_folder):
			dir = os.listdir(output_folder)
			if "RESULTS" or "RESULTS_FASTA" or "output.log" in dir:
				print("#################################################################################################")
				print("This output folder already contains data from a previous run. Please choose another output folder")
				print("#################################################################################################")
				sys.exit(1)
			else:
				pass
		else:
			os.system("mkdir -p {}".format(output_folder))
			
	#Type strain parameter
	if arguments[argument].startswith("-T") or arguments[argument].startswith("--type"):
		typestrain = True
	#User specified genus
	if arguments[argument].startswith("-G") or arguments[argument].startswith("--genus"):
		genus = arguments[argument+1]
		genus = genus.lower()
		genus = "".join(genus.split())
	#Maximial percent length threshold
	if arguments[argument].startswith("--max"):
		max_thres_set = arguments[argument+1]
	#Minimial percent length threshold
	if arguments[argument].startswith("--min"):
		min_thres_set = arguments[argument+1]	
	#Minimial percentage amount of original genes to be prophage
	if arguments[argument].startswith("--genes"):
		min_genes_set = arguments[argument+1]
	#Minimial percentage amount of original genes to be a gap
	if arguments[argument].startswith("--gap"):
		gap_thres_set = arguments[argument+1]
	#Percent identity used in BLAST
	if arguments[argument].startswith("-i") or arguments[argument].startswith("--identity"):
		identity = arguments[argument+1]
	#Percent identity used in BLAST
	if arguments[argument].startswith("-cov") or arguments[argument].startswith("--coverage"):
		coverage = arguments[argument+1]
	#Max amount of cores
	if arguments[argument].startswith("-cor") or arguments[argument].startswith("--cores"):
		cores = arguments[argument+1]
		
	
try:
	print("Will work with genus: " + str(genus))
except NameError as error:
	print("Genus not defined. Use --genus or print help index with -h")
	sys.exit(1)
	
#set database PATH
os.system("set BLASTDB ="+str(scripts)+"../db:$BLASTDB")

#search for database at the expected location
database_present = False
for dire in os.listdir(scripts):
	if dire == "db":
		for database in os.listdir(scripts+"/db"):
			if typestrain == True:
				if database.startswith(genus + "T"):
					database_present = True
			else:
				if database.startswith(genus) and not database.startswith(genus + "T"):
					database_present = True
				
#If database not present, download it
if database_present == False:
	os.chdir(scripts+"/database_fastas")
	good_genus = False
	download_error = False
	missing = False
	
	#Download database 
	while good_genus == False:
		print("Downloading database for you. This might take some time.")
		if typestrain == True:
			print("Only downloading type strains.")
			command = "ncbi-genome-download -F 'fasta' -l 'complete' -M  'type' --genus " + str(genus) + " bacteria -p "+str(int(cores)*2)+" -r 1 2> errors.txt"
			try:
				output = subprocess.check_output(command, shell=True)
			except Exception as error:
				with open("errors.txt","r") as er_file:
					for line in er_file:
						if "MissingSchema" in line:
							missing = True
				if missing == False:
					download_error = True
				print(error)
				break
			good_genus = True
		else:
			command = "ncbi-genome-download -F 'fasta' -l 'complete' --genus " + str(genus) + " bacteria -p "+str(int(cores)*2)+" -r 1 2> errors.txt"
			try:
				output = subprocess.check_output(command, shell=True)
			except Exception as error:
				with open("errors.txt","r") as er_file:
					for line in er_file:
						if "MissingSchema" in line:
							missing = True
				if missing == False:
					download_error = True
				print(error)
				break
			good_genus = True
			
	if missing == True:
		fna_count = 0
		for folder in os.listdir("refseq/bacteria/"):
			for fna in os.listdir("refseq/bacteria/"+folder):
				if fna.endswith("fna.gz"):
					fna_count += 1
		print("The amount of properly downloaded fasta files is: " + str(fna_count))
	
		if fna_count > 1:
			print("Will work with the proper downloaded files")
		else:	
			print("Not enough to build a proper database. Shutting down.")
			sys.exit(1)

	elif download_error == True: 
		print("Something went wrong while downloading the database fasta files.\n Please try again later or with another genus.")
		sys.exit(1)
		
	#Collecting both individual fastas and all fastas in one file
	if typestrain == True:
		os.system("cat refseq/bacteria/**/*.fna.gz >> " + str(genus) + "T_DNA_cds.fna.gz")
	else:
		os.system("cat refseq/bacteria/**/*.fna.gz >> " + str(genus) + "_DNA_cds.fna.gz")
	os.system("mv refseq/bacteria/**/*.fna.gz ./")
	os.system("gunzip *.gz | parallel -j {}".format(cores))
	
	#Make database format
	print("making database files")
	if typestrain == False:
		command = "ls *fna | parallel -j {} 'makeblastdb -in {} -dbtype nucl -parse_seqids -out ../db/{}/{}_DNA_DB' >/dev/null 2>&1".format(cores,fasta,genus,fasta)
		os.system(command)
		with open("../db/"+str(genus)+"/database_names.txt",'a') as names:		#Make list with all individual database names
			if fasta != str(genus) + "_DNA_cds.fna":
				names.write(fasta + "_DNA_DB\n")
		
	else:
		command = "ls *fna | parallel -j {} 'makeblastdb -in {} -dbtype nucl -parse_seqids -out ../db/{}/{}_DNA_DB' >/dev/null 2>&1".format(cores,fasta,genus,fasta)
		os.system(command)
		with open("../db/"+str(genus)+"T/database_names.txt",'a') as names:		#Make list with all individual database names
			if fasta != str(genus) + "T_DNA_cds.fna":
				names.write(fasta + "_DNA_DB\n")
			
			
	os.chdir("..")			

		
#Run add-ons 
if "-a" in sys.argv[1:]:
	with open(scripts+"/scripts/attachment.txt",'w') as attachment:
		attachment.write("\nadd_on = True\n#import packages and setting working directory\nimport os\noutput_folder = \"{}\"\nfasta_folder = \"{}\"\n\n\nscripts = \"{}/scripts\"\n".format(output_folder,fasta_folder,scripts))
	command = "cat {}/scripts/attachment.txt {}/snakefile.py >> {}/snakefile_run.py".format(scripts, scripts, scripts)
	os.system(command)
	os.system("chmod a+x {}/snakefile.py".format(scripts))
	command = "cat {}/scripts/attachment.txt {}/scripts/script1.0.py >> {}/scripts/phylogeny_display.py".format(scripts, scripts, scripts)
	os.system(command)
else:
	with open(scripts+"/scripts/attachment.txt",'w') as attachment:
		attachment.write("\nadd_on = False\n#import packages and setting working directory\nimport os\noutput_folder = \"{}\"\nfasta_folder = \"{}\"\n\nscripts = \"{}/scripts\"\n".format(output_folder,fasta_folder,scripts))
	command = "cat {}/scripts/attachment.txt {}/snakefile.py >> {}/snakefile_run.py".format(scripts,scripts,scripts)
	os.system(command)
	os.system("chmod a+x {}/snakefile.py".format(scripts))
	command = "cat {}/scripts/attachment.txt {}/scripts/script1.0.py >> {}/scripts/phylogeny_display.py".format(scripts,scripts,scripts)
	os.system(command)
	os.system("chmod a+x {}/scripts/phylogeny_display.py".format(scripts))
	
					
#Define genus in blast script
if typestrain == True:
	genus = genus + "T"
else:
	pass 

with open(scripts+"/scripts/attachment.txt",'w') as attachment:
	attachment.write("\ngenus = \"" + str(genus) + "\"\ndatabase_name=\"" + str(genus) + "_DNA_cds.fna_DNA_DB\" \nscripts = \"{}/scripts\"".format(scripts))
command = "cat {}/scripts/attachment.txt {}/scripts/script2.0.py >> {}/scripts/blast_pre.py".format(scripts,scripts,scripts)
os.system(command)

os.system("chmod a+x {}/scripts/blast_pre.py".format(scripts))
with open(scripts+"/scripts/attachment.txt",'w') as attachment:
	attachment.write("\ngenus = \"" + str(genus) + "\"\ndatabase_name=\"" + str(genus) + "_DNA_cds.fna_DNA_DB\" \n")
command = "cat {}/scripts/attachment.txt {}/scripts/script4.0.py >> {}/scripts/collection_host.py".format(scripts,scripts,scripts)
os.system(command)
os.system("chmod a+x {}/scripts/collection_host.py".format(scripts))

#Prepare restart script  
with open(scripts+"/restart_prep.txt","w") as restart_prep:
	restart_prep.write("\nfasta_folder = \"{}\"\noutput_folder = \"{}\"\nscripts = \"{}\"\n".format(fasta_folder,output_folder,scripts))
command = "cat {}/restart_prep.txt {}/restart_end.py > {}/restart.py".format(scripts,scripts,scripts)
os.system(command)


#Prepare cleanup script
with open(scripts+"/cleanup_prep.txt","w") as cleanup_prep:
	cleanup_prep.write("#!/bin/bash\nfasta_folder=\"${}\"\noutput_folder=\"${}\"\nscripts=\"${}\"\n".format(fasta_folder,output_folder,scripts))
command = "cat {}/cleanup_prep.txt {}/cleanup_end.sh > {}/cleanup.sh".format(scripts,scripts,scripts)
os.system(command)

		


#Ascribe user setting 

#Test numericallity of user setting
try:
	float(identity)
	float(coverage)
	float(max_thres_set)
	float(min_thres_set)
	float(min_genes_set)
	float(gap_thres_set)
except ValueError as error:
	print("All values, except genus, has to be numerical. Please try again.")
	sys.exit(1)
		
	#BLAST thresholds with sanity check 
	#Percent identity
while float(identity) < 15:
	print("Your identity is too low. This would give random results")
	identity = str(input("enter new BLAST percent identity : "))
#Query coverage
while float(coverage) < 15:
	print("your coverage is too low, this would give random results")
	coverage = str(input("enter new BLAST percent query coverage : "))
		

#If any negative threshold, please reenter
while float(max_thres_set) < 0:
	print("A negative threshold is not possible. Please reenter.")
	max_thres_set = str(input("\nMaximal percent length relative to average of original samples: "))
while float(min_thres_set) < 0:
	print("A negative threshold is not possible. Please reenter.")
	min_thres_set = str(input("\nMinimal percent length relative to average of original samples: "))
while float(min_genes_set) < 0:
	print("A negative threshold is not possible. Please reenter.")
	min_genes_set = str(input("\nMinimal amount of the orignial genes that should be present in a putative phage : "))
while float(gap_thres_set) < 0:
	print("A negative threshold is not possible. Please reenter.")
	gap_thres_set = str(input("\nMinimal percent of unknown genes in a phage that in a continous stretch would indicate a gap : "))

#Check if unreasonable threshold was intended (short hits)
if float(max_thres_set)<100:
	print("Notice: A threshold below 100 would filter out identical phages and limit findings.\nFor sanity check, please reenter.")
	max_thres_set = str(input("please reenter maximal percent length relative to average of original samples: "))

#Max must be higher than min
while float(max_thres_set) < float(min_thres_set):
	print("The maximal length threshold cannot be smaller than the minimal length threshold. Please reenter")
	max_thres_set = str(input("Maximal percent length relative to average of original samples: "))
	min_thres_set = str(input("Minimal percent length relative to average of original samples: "))
		
#Check if unreasonable threshold was intended (long hits)	
if float(min_thres_set) > 100:
	print("\nNotice: A threshold above 100 would filter out identical phages and limit findings.\nFor sanity check, please reenter.")
	min_thres_set = str(input("Minimal percent length relative to average of original samples: "))

#No more than 100% of genes are possible
while float(min_genes_set)>100:
	print("Not possible to have a minimal above 100% of the genes. Please correct.")
	min_genes_set = str(input("Minimal amount of the orignial genes that should be present in a putative phage : "))

#Check if unreasonable threshold was intended (long gaps)
if float(gap_thres_set) > 50:
	print("A gap threshold measuring more than 50% of the total amount of genes is not advised. Default setting at 15.\nFor sanity check, please reenter.")
	gap_thres_set = str(input("Minimal percent of unknown genes in a phage that in a continous stretch would indicate a gap : "))

	
#Write an attachment and attach to script	
with open(scripts+"/scripts/attachment.txt",'w') as attachment:
	attachment.write("\nidentity = "+str(identity)+"\ncoverage = "+str(coverage)+"\nmax_thres_set = "+str(max_thres_set)+"\nmin_thres_set = "+str(min_thres_set)+"\nmin_genes_set = "+str(min_genes_set)+"\ngap_thres_set = "+str(gap_thres_set))

command = "cat {}/scripts/attachment.txt {}/scripts/blast_pre.py >> {}/scripts/blast.py".format(scripts,scripts,scripts)
os.system(command)
os.system("chmod a+x {}/scripts/blast.py".format(scripts))
command = "cat {}/scripts/attachment.txt {}/scripts/script3.0.py >> {}/scripts/filter.py".format(scripts,scripts,scripts)
os.system(command)
os.system("chmod a+x {}/scripts/filter.py".format(scripts))

#Check the right filetypes
fasta_count = 0
error_flag = False

try:
	os.chdir(fasta_folder)
except OSError:
	print("The specified fasta folder does not exist.")
	sys.exit(1)
	
	
for documents in os.listdir(fasta_folder):
	
	#count all fasta documents
	if documents.endswith(".fas") or documents.endswith(".fsa") or documents.endswith(".fasta") or documents.endswith(".fna"):
		fasta_count += 1
		
		#Open all fasta documents
		with open(documents, 'r') as fasta:

			#Check if header is in right format
			header = fasta.readline()
			line_ending = header[-1]
			if not header.startswith(">"):
				print("Something is wrong with your header in file " + str(documents))
				error_flag = True
				
			#Check if sequence is in right format
			sequence = fasta.readline()[:-1]
			sequence_errors = re.search(r"[^atgcATGC]", sequence)
			if not sequence_errors is None:
				print("Something is wrong with your sequence in file " + str(documents))
				error_flag = True
				
		#Make sure all line endings follow Linux format
		if error_flag == False:		
			with open(documents, 'r') as fasta_correct:
				fasta_content = fasta_correct.read()
			new_content = fasta_content.replace(line_ending, "\n")
			with open("accepted"+documents[:-4]+".fna",'w') as accepted:
				accepted.write(new_content)
			os.remove(documents)
				
			
#Stop if there are errors in the sequences		
if fasta_count == 0:
	raise IOError("No fasta files where available. Check you placement of the files or the file extensions")
	sys.exit(1)
elif error_flag == True:
	raise IOError("Due to errornous fasta files, the process cannot be continued")
	sys.exit(1)

#Move the analysis to proper folder
os.system("mv {}/* {}".format(fasta_folder, scripts))
print("-------------------------------------------------------------------------------")
print("Initializing is done")
print("-------------------------------------------------------------------------------")
