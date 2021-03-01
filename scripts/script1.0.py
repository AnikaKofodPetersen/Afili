

#import packages
import os
import re


#define initial values
species = "-"
ST = "-"

#Making color scheme (one color for each ST)
with open("SpeciesMetadata.txt", 'a') as metadata:						#Prepare Species metadata file
	metadata.write("Name\tSpecies/ST\n")
	
with open("host_mlst.txt", 'r') as host_mlst:
	for line in host_mlst:
		species = line.split()[1]
		ST = line.split()[2]

		fasta_num = line.split()[0]										#register the number associated with the host fasta
		fasta_num = fasta_num.split("fasta")[2].split(".")[0]
		
		with open("host_fastas/name_storage.txt", 'r') as name_storage:
			for name_line in name_storage:
				num_name = name_line.split()[0]

				if num_name == fasta_num:								#find the accessionnumber associated with the host number
					acc = name_line.split()[1]
					
		with open("collected_phages/collected_all", 'r') as cfc:
			ST_set = set()												#collect all prophage names that would come from hosts of the same ST
			for fasta_line in cfc:
				if fasta_line.startswith(">"):
					entry = fasta_line[1:]

					if acc in entry:
						ST_set.add(entry.split()[0])
						

		with open("SpeciesMetadata.txt", 'a') as metadata:				#Write the color map for the phylogenetic display, one ST at the time for all the collected prophages
			for label in ST_set:
				label = re.sub(r'[^\d+[_]\d+[_]\w*_*\.*]', "_", label, count=0)
				metadata.write(str(label) + "\t" + str(species) + "_" + str(ST)+"\n")


	
#Making an ornament map if antismash is requested
if add_on == True:
	pass


#making ornaments for the original ppBGCs
with open("originalsMetadata.txt", 'a') as originals:
	originals.write("Name\tOriginal\n")
with open("original_names.txt", 'r') as names:
	for line in names:
		with open("originalsMetadata.txt", 'a') as originals:
			originals.write(str(line)[:-1]+ "\tYES\n")
			


#Moving phylogenetic maps
os.mkdir("newick_trees")
os.system("mv originalsMetadata.txt newick_trees")
if add_on == True:
	pass
os.system("mv SpeciesMetadata.txt newick_trees")

#Make ending indicator
os.system("touch phylogeny_display_done")
