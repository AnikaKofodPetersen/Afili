

#import packages and change directory
import os
import copy
import sys

os.chdir("blast_folder")

#Calculate thresholds
file_count = 0
sum_length = 0

for files in os.listdir(".."):
	if files.endswith(".fna"):						#Find all original ppBGC fastas
		file_count += 1								#Count originals
		with open("../"+files, 'r') as original_fasta:
			sequence = ""
			header = original_fasta.readline()
			
			for line in original_fasta:
				sequence += str(line)				#Find the sequence of the original 
			sequence = "".join(sequence.split())
			sum_length += len(sequence)				#Sum all original lengths		

ave_length = sum_length/file_count					#Average length of original
max_length = ave_length*(float(max_thres_set)/100)	#Max length threshold
min_length = ave_length*(float(min_thres_set)/100)	#Min length threshold


#Find original gene count
gene_dict = dict()
for files in os.listdir():
	if files.endswith(".ffn"):						#Find all ffn_files
		with open(files, 'r') as ffn_file:
			gene_count = 0
			for line in ffn_file:
				if line.startswith(">"):
					gene_count += 1					#Save gene count in dictionary with ffn number as key
			gene_dict[files[:-4]] = gene_count

				
#Find potential prophages
predicted_phages = dict()							#Create dictionary for predicted phages
for blast in os.listdir():
	if blast.endswith("DNA_DB_blast"):
		number = blast.split(".")[0]				#Save identity number to associate with ffn file
		with open(blast, 'r') as blast_output:		#Check all blast outputs
			gene_start = []
			gene_end = []
			for line in blast_output:
				if len(line) != 0:					#All non-empty blast outputs, collect gene positions
					accession = line.split()[1]
					if line.split()[8] < line.split()[9]:
						gene_start += [int(line.split()[8])]
						gene_end += [int(line.split()[9])]
					else:
						gene_start += [int(line.split()[9])]
						gene_end += [int(line.split()[8])]
						
					ordered_start = sorted(gene_start)
					ordered_end = sorted(gene_end)

				
					
					cuts_start = [0]								
					cuts_end = []
					phage_genes = []
					gene_count = 0
					
					for position in range(1,len(ordered_start)):		#Cut the start and end positions if big gaps appear
						gene_count += 1
						if float(ordered_start[position]) > float(ordered_end[position-1])+(float(gene_dict[number])/100)*1000*float(gap_thres_set):
								phage_genes += [gene_count]
								cuts_start += [position]
								cuts_end += [position-1]
								gene_count = 0
					cuts_end +=[len(ordered_end)-1]
					phage_genes += [gene_count]
						


			
					gene_iter = iter(phage_genes)			#iterator through gene counts for each predicted phage
					phage_count = 0
					for position in range(0, len(cuts_start)):	#Save predicted phages in dictionary
						phage_count += 1
						entry = str(number)+"_"+str(phage_count)+"_phage_"+str(accession)
						predicted_phages[entry] = {}	#new entry for eahc new phage
						predicted_phages[entry]["number"] = number
						predicted_phages[entry]["all_genes"] = gene_dict[number]
						predicted_phages[entry]["genes"] = next(gene_iter)
						predicted_phages[entry]["start"] = ordered_start[cuts_start[position]]
						predicted_phages[entry]["end"] = ordered_end[cuts_end[position]]


#Deep copy the predicted phages 
deep_copy = copy.deepcopy(predicted_phages)


#Perform the filtering
total_before = 0
total_after = 0
gene_filter = 0
max_length_filter = 0
min_length_filter = 0
for entry in deep_copy:
	total_before += 1
	if float(deep_copy[entry]["genes"]) < float(gene_dict[deep_copy[entry]["number"]])*(float(min_genes_set)/100):
		del predicted_phages[entry]
		gene_filter += 1
		#print("Phage deleted because of gene amount")
	elif float(deep_copy[entry]["end"])-float(deep_copy[entry]["start"]) > max_length:
		del predicted_phages[entry]
		max_length_filter += 1
		#print("Phage deleted because of max length")
	elif float(deep_copy[entry]["end"])-float(deep_copy[entry]["start"]) < min_length:
		del predicted_phages[entry]
		min_length_filter += 1
		#print("Phage deleted because of min length")
total_after = total_before - gene_filter - max_length_filter - min_length_filter
		
print("TOTAL_BEFORE: {}  TOTAL_AFTER: {}   GENE_FILER: {}  MAX_LENGTH: {}   MIN_LENGTH: {}".format(total_before,total_after,gene_filter,max_length_filter,min_length_filter))
print("Average length of originals: " + str(ave_length) + "\n")
print("Max length threshold: " + str(max_length) + "\n")
print("Min length threshold: " + str(min_length) + "\n")
print("Number of predicted matches to the query: " +str(len(predicted_phages)))
#Make a 0-error
if len(predicted_phages) == 0:
	print("#########################################################################\n\n\n")
	print("NO MATCHES FOUND\n\n\n")
	print("There where no homologue matches in the database to your query.")
	print("Will not be able to produce the neccessary files. \n\n\n")
	print("########################################################################\n\n\n")
	os.system("touch ../end_snakemake")
	os.chmod("../end_snakemake", 0o777)
	os.system("touch ../filtering_done")
	os.system("touch ../collected_analysis_done")
	os.system("touch ../phylogeny_display_done")
	os.system("touch ../heatmaps_done")
	os.system("touch ../all_done")
	sys.exit(1)
	
#Check for impossible phylogeny
elif len(predicted_phages) == 1:
	print("#########################################################################\n\n\n")
	print("ONLY ONE MATCH FOUND\n\n\n")
	print("With only one match, no phylogeny will be calculated.")
	print("Will not be able to produce a newick tree file.\n\n\n")
	print("########################################################################\n\n\n")
	os.system("touch ../skip_phylogeny")
	
	#Write outputfile with accepted phages			
	with open("accepted_phages.txt",'a') as accepts:
		for entry in predicted_phages:
			total_before += 1
			total_after += 1
			accepts.write(entry + "\t")
			accepts.write(str(predicted_phages[entry]["start"]) + "\t")
			accepts.write(str(predicted_phages[entry]["end"]) + "\t")
			accepts.write("\n")
	#Make log file				
	with open("../ThresholdPhageLog.txt",'a') as output:
		output.write("Before filter total amount of phages: " + str(total_before) + "\n")
		output.write("After filter total amount of phages: " + str(total_after) + "\n")
		output.write("Caugth by gene filter: " + str(gene_filter) + "\n")
		output.write("Caugth by max length filter: " + str(max_length_filter) + "\n")
		output.write("Caugth by min filter: " + str(min_length_filter) + "\n")
		output.write("Average length of originals: " + str(ave_length) + "\n")
		output.write("Max length threshold: " + str(max_length) + "\n")
		output.write("Min length threshold: " + str(min_length) + "\n")
		
	#Save phage coordinates and completeness
	complete = open("../phage_completeness.txt","a")
	with open("../phage_coordinates.txt","a") as coordinates:
		coordinates.write("Phage_label\tcoordinates\n")
		complete.write("Phage_label\tfullfillment of original genes\n")
		for i in predicted_phages.items():
			print(i[0]+"\t"+str(i[1]["start"])+"..."+str(i[1]["end"])+"\t"+str(i[1]["genes"])+"/"+str(i[1]["all_genes"]))
			coordinates.write(i[0]+"\t"+str(i[1]["start"])+"..."+str(i[1]["end"])+"\n")
			complete.write(i[0]+"\t"+str(i[1]["genes"])+"/"+str(i[1]["all_genes"])+"\n")
	complete.close()
				


	#Make ending indicator
	os.system("touch ../filtering_done")


else:
	
	#Write outputfile with accepted phages			
	with open("accepted_phages.txt",'a') as accepts:
		for entry in predicted_phages:
			total_before += 1
			total_after += 1
			accepts.write(entry + "\t")
			accepts.write(str(predicted_phages[entry]["start"]) + "\t")
			accepts.write(str(predicted_phages[entry]["end"]) + "\t")
			accepts.write("\n")
	#Make log file				
	with open("../ThresholdPhageLog.txt",'a') as output:
		output.write("Before filter total amount of phages: " + str(total_before) + "\n")
		output.write("After filter total amount of phages: " + str(total_after) + "\n")
		output.write("Caugth by gene filter: " + str(gene_filter) + "\n")
		output.write("Caugth by max length filter: " + str(max_length_filter) + "\n")
		output.write("Caugth by min filter: " + str(min_length_filter) + "\n")
		output.write("Average length of originals: " + str(ave_length) + "\n")
		output.write("Max length threshold: " + str(max_length) + "\n")
		output.write("Min length threshold: " + str(min_length) + "\n")
		
	#Save phage coordinates and completeness
	complete = open("../phage_completeness.txt","a")
	with open("../phage_coordinates.txt","a") as coordinates:
		coordinates.write("Phage_label\tcoordinates\n")
		complete.write("Phage_label\tfullfillment of original genes\n")
		for i in predicted_phages.items():
			print(i[0]+"\t"+str(i[1]["start"])+"..."+str(i[1]["end"])+"\t"+str(i[1]["genes"])+"/"+str(i[1]["all_genes"]))
			coordinates.write(i[0]+"\t"+str(i[1]["start"])+"..."+str(i[1]["end"])+"\n")
			complete.write(i[0]+"\t"+str(i[1]["genes"])+"/"+str(i[1]["all_genes"])+"\n")
	complete.close()
				


	#Make ending indicator
	os.system("touch ../filtering_done")

